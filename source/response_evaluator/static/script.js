let files = [];
let allResponses = [];

function showResults() {
    document.getElementById('result-rendering-title').style.display = 'block';
}

function showEvaluation() {
    document.getElementById('evaluation-summary').style.display = 'block';
}

function handleFiles() {
    const input = document.getElementById('file-input');
    files = input.files;
    const fileBox = document.getElementById('file-box');

    if (files.length > 0) {
        fileBox.textContent = files.length + " file(s) selected";
        document.getElementById('file-box').classList.add('file-selected');
    } else {
        document.getElementById('file-box').classList.remove('file-selected');
    }
}

document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const formData = new FormData();
    Array.from(fileInput.files).forEach(file => {
        formData.append('files', file);
    });

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Processing, please wait...</p>';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (!data.responses) {
            throw new Error('No responses found in server response');
        }

        allResponses = data.responses;
        populateFilters(allResponses);

        showResults();
        applyFilters();

        showDownloadAndSubmitOptions(data.response_filename, data.responses);

    } catch (error) {
        resultsDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
    }
};

function populateFilters(responses) {
    const viewtypeFilter = document.getElementById('viewtype-filter');
    const libraryFilter = document.getElementById('library-filter');

    viewtypeFilter.innerHTML = '<h4>View Type:</h4>';
    libraryFilter.innerHTML = '<h4>Library:</h4>';

    const viewtypes = [...new Set(responses.map(r => r.view_type))];
    const libraries = [...new Set(responses.map(r => r.library))];

    generateFilterButton(viewtypeFilter, 'viewtype', viewtypes);
    generateFilterButton(libraryFilter, 'library', libraries);

    document.getElementById('filters').style.display = 'flex';
}

function generateFilterButton(container, filterType, options) {
    options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option;
        button.classList.add('filter-button');
        button.setAttribute('data-filter', filterType);

        button.addEventListener('click', function() {
            button.classList.toggle('selected');
            updateFilters(filterType, option);
            applyFilters();
        });

        container.appendChild(button);
    });
}

let selectedFilters = {
    viewtype: [],
    library: []
};

// update filter requirement
function updateFilters(filterType, filterValue) {
    const index = selectedFilters[filterType].indexOf(filterValue);
    if (index === -1) {
        selectedFilters[filterType].push(filterValue);
    } else {
        selectedFilters[filterType].splice(index, 1);
    }
}

function applyFilters() {
    const viewtypeValue = selectedFilters.viewtype;
    const libraryValue = selectedFilters.library;

    const filteredResponses = allResponses.filter(r => {
        const matchesViewType = viewtypeValue.length === 0 || viewtypeValue.includes(r.view_type);
        const matchesLibrary = libraryValue.length === 0 || libraryValue.includes(r.library);

        return matchesViewType && matchesLibrary ;
    });

    displayResponses(filteredResponses);
}

// show response
function displayResponses(responses) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    showResults();

    responses.forEach((response) => {  // 移除 index 参数
        const container = document.createElement('div');
        container.className = 'iframe-container';

        const title = document.createElement('h3');
        title.textContent = `${response.title}`;
        title.style.textAlign = 'center';

        const iframe = document.createElement('iframe');
        iframe.srcdoc = response.response;

        const viewDetailsButton = document.createElement('button');
        viewDetailsButton.textContent = 'View Details';
        viewDetailsButton.onclick = () => {
            window.open(`/view_response?index=${response.originalIndex}`, '_blank');
        };

        const evaluationForm = document.createElement('div');
        evaluationForm.className = 'evaluation-container';
        evaluationForm.dataset.originalIndex = response.originalIndex;

        const evaluationOptions = ['Correct', 'Initialization Error', 'Unexpected Initial Result', 'Execution Error', 'Unexpected Execution Result'];
        let evaluationString = response.evaluation;
        evaluationOptions.forEach(option => {
            const isChecked = evaluationString.includes(option);
            evaluationForm.innerHTML += `
                <label class="evaluation-option">
                    <input type="checkbox" name="evaluation${response.originalIndex}" value="${option}" ${isChecked ? 'checked' : ''}>
                    <span>${option}</span>
                </label>
            `;
        });

        container.appendChild(title);
        container.appendChild(iframe);
        container.appendChild(viewDetailsButton);
        container.appendChild(evaluationForm);
        resultsDiv.appendChild(container);
    });
}

function showDownloadAndSubmitOptions(responseFilename, responses) {
    const submitButtonContainer = document.getElementById('submit-evaluation-container');
    submitButtonContainer.style.display = 'flex';

    const finishAllButtonContainer = document.getElementById('finish-all-container');
    finishAllButtonContainer.style.display = 'flex';

    submitButtonContainer.querySelector('#submit-evaluation').onclick = async function() {
        const evaluations = [];
        const evaluationForms = document.querySelectorAll('.evaluation-container');

        evaluationForms.forEach((form) => {
            const originalIndex = parseInt(form.dataset.originalIndex, 10);
            const selectedOptions = Array.from(form.querySelectorAll(`input[name="evaluation${originalIndex}"]:checked`))
                                        .map(input => input.value);
            evaluations.push({ responseIndex: originalIndex, evaluation: selectedOptions });
        });

        console.log('Submitting evaluations:', evaluations);

        try {
            const evalResponse = await fetch('/submit_evaluation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ evaluations, responseFilename }),
            });

            const evalData = await evalResponse.json();

            if (evalResponse.ok) {
                alert('Evaluation submitted and saved!');
            } else {
                alert(`Error: ${evalData.error || 'Unknown error occurred.'}`);
            }
        } catch (error) {
            console.error('Error submitting evaluation:', error);
            alert('An error occurred while submitting evaluation.');
        }
    };

    finishAllButtonContainer.querySelector('#finish-all').onclick = async function() {
        try {
            const response = await fetch(`/finalize/${responseFilename}`, {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Failed to finalize the file.');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = responseFilename;
            document.body.appendChild(a);
            a.click();
            a.remove();

            alert('Final file has been downloaded!');

            const showEvaluationContainer = document.getElementById('show-evaluation-container');
            showEvaluationContainer.style.display = 'flex';

            disableEvaluation();

        } catch (error) {
            console.error('Error finalizing file:', error);
            alert('An error occurred while finalizing the file.');
        }
    };
}

function disableEvaluation() {
    const evaluationForms = document.querySelectorAll('.evaluation-container');
    evaluationForms.forEach(form => {
        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = true;
        });
    });

    const submitButtonContainer = document.getElementById('submit-evaluation-container');
    submitButtonContainer.style.display = 'none';

    const finishAllButtonContainer = document.getElementById('finish-all-container');
    finishAllButtonContainer.style.display = 'none';
}
