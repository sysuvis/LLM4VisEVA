let csvData = [];
let filteredData = [];
let chart = null; // Global chart instance

// Display and bind “Show Evaluation”
document.getElementById('show-evaluation-button').onclick = function() {
    document.getElementById('evaluation-summary').style.display = 'flex';
    fetchEvaluationData();
};

// Fetch the evaluation data from the backend
function fetchEvaluationData() {
    axios.get('/evaluation_chart')
        .then(response => {
            console.log("Received data:", response.data);

            if (Array.isArray(response.data)) {
                csvData = response.data;
                filteredData = csvData;
                updateChartFilters();
                calculateErrorRates();
            } else {
                console.error("Received data is not an array:", response.data);
                alert("Failed to load evaluation data: Data format error.");
            }
        })
        .catch(error => {
            console.error("Error fetching evaluation data:", error);
            alert("Failed to load evaluation data.");
        });
}

// Update filters based on CSV data
function updateChartFilters() {
    console.log("csvData:", csvData);

    document.getElementById('viewTypeFilter').innerHTML = '';
    document.getElementById('libraryFilter').innerHTML = '';

    const viewTypes = new Set();
    const libraries = new Set();

    csvData.forEach(row => {
        viewTypes.add(row.view_type);
        libraries.add(row.library);
    });

    // Populate View Type Filter (checkboxes)
    const viewTypeContainer = document.getElementById('viewTypeFilter');
    viewTypes.forEach(viewType => {
        const label = document.createElement('label');
        label.className = "form-check-label";
        label.innerHTML = viewType;
        const checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.className = "form-check-input";
        checkbox.value = viewType;
        checkbox.addEventListener('change', filterData);

        const div = document.createElement('div');
        div.className = "form-check";
        div.appendChild(checkbox);
        div.appendChild(label);
        viewTypeContainer.appendChild(div);
    });

    // Populate Library Filter (checkboxes)
    const libraryContainer = document.getElementById('libraryFilter');
    libraries.forEach(library => {
        const label = document.createElement('label');
        label.className = "form-check-label";
        label.innerHTML = library;
        const checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.className = "form-check-input";
        checkbox.value = library;
        checkbox.addEventListener('change', filterData);

        const div = document.createElement('div');
        div.className = "form-check";
        div.appendChild(checkbox);
        div.appendChild(label);
        libraryContainer.appendChild(div);
    });
}

// Filter data based on selected checkboxes
function filterData() {
    const selectedViewTypes = Array.from(document.querySelectorAll('#viewTypeFilter input:checked')).map(input => input.value);
    const selectedLibraries = Array.from(document.querySelectorAll('#libraryFilter input:checked')).map(input => input.value);

    filteredData = csvData.filter(row => {
        const matchesViewType = selectedViewTypes.length === 0 || selectedViewTypes.includes(row.view_type);
        const matchesLibrary = selectedLibraries.length === 0 || selectedLibraries.includes(row.library);
        return matchesViewType && matchesLibrary;
    });

    calculateErrorRates();
}

// Calculate error rates and statistics
function calculateErrorRates() {
    const counts = {
        initError: 0,
        unexpectedInit: 0,
        execError: 0,
        correct: 0,
        unexpectedExec: 0
    };
    let totalCount = 0;

    filteredData.forEach(row => {
        if (row.evaluation) {
            totalCount++;
            if (row.evaluation === 'Initialization Error') counts.initError++;
            if (row.evaluation === 'Unexpected Initial Result') counts.unexpectedInit++;
            if (row.evaluation === 'Execution Error') counts.execError++;
            if (row.evaluation === 'Correct') counts.correct++;
            if (row.evaluation === 'Unexpected Execution Result') counts.unexpectedExec++;
        }
    });

    // Calculate and display error rates as percentages
    const initErrorRate = (counts.initError / totalCount * 100).toFixed(2);
    const unexpectedInitRate = (counts.unexpectedInit / totalCount * 100).toFixed(2);
    const execErrorRate = (counts.execError / totalCount * 100).toFixed(2);
    const correctRate = (counts.correct / totalCount * 100).toFixed(2);
    const unexpectedExecRate = (counts.unexpectedExec / totalCount * 100).toFixed(2);

    // Display error rates
    document.getElementById('initErrorRate').textContent = `${initErrorRate}%`;
    document.getElementById('unexpectedInitRate').textContent = `${unexpectedInitRate}%`;
    document.getElementById('execErrorRate').textContent = `${execErrorRate}%`;
    document.getElementById('correctRate').textContent = `${correctRate}%`;
    document.getElementById('unexpectedExecRate').textContent = `${unexpectedExecRate}%`;

    // Update progress bars with smooth animations
    document.getElementById('initErrorProgress').style.width = `${initErrorRate}%`;
    document.getElementById('unexpectedInitProgress').style.width = `${unexpectedInitRate}%`;
    document.getElementById('execErrorProgress').style.width = `${execErrorRate}%`;
    document.getElementById('correctRateProgress').style.width = `${correctRate}%`;
    document.getElementById('unexpectedExecProgress').style.width = `${unexpectedExecRate}%`;

    // Update the chart
    updateChart();
}

// Update the chart with error data
function updateChart() {
    const groupedData = {};

    // Group by library and view_type
    filteredData.forEach(row => {
        const key = `${row.library}-${row.view_type}`;
        if (!groupedData[key]) {
            groupedData[key] = { initError: 0, unexpectedInit: 0, execError: 0, correct: 0, unexpectedExec: 0 };
        }

        if (row.evaluation === 'Initialization Error') groupedData[key].initError++;
        if (row.evaluation === 'Unexpected Initial Result') groupedData[key].unexpectedInit++;
        if (row.evaluation === 'Execution Error') groupedData[key].execError++;
        if (row.evaluation === 'Correct') groupedData[key].correct++;
        if (row.evaluation === 'Unexpected Execution Result') groupedData[key].unexpectedExec++;
    });

    const labels = Object.keys(groupedData);

    const colorPalette = [
        "#5470c6", "#91cc75", "#fac858", "#ee6666",
        "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"
    ];

    const datasets = [
        { label: 'Initialization Error', data: [], backgroundColor: colorPalette[0] },
        { label: 'Unexpected Initial Result', data: [], backgroundColor: colorPalette[1] },
        { label: 'Execution Error', data: [], backgroundColor: colorPalette[2] },
        { label: 'Correct', data: [], backgroundColor: colorPalette[3] },
        { label: 'Unexpected Execution Result', data: [], backgroundColor: colorPalette[4] }
    ];

    labels.forEach(label => {
        const data = groupedData[label];
        datasets[0].data.push(data.initError);
        datasets[1].data.push(data.unexpectedInit);
        datasets[2].data.push(data.execError);
        datasets[3].data.push(data.correct);
        datasets[4].data.push(data.unexpectedExec);
    });

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(document.getElementById('evaluationChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });
}
