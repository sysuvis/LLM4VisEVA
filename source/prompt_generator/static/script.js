new Vue({
    el: '#app',
    data: {
        datasetDescription: '',
        selectedLibrary: '', 
        selectedView: '',    
        showModal: false,
        configOutput: '',
        selectedFile: null,  // For upload file
        responseFileName: '',  // Save response file name
        responseDownloadLink: ''  // Save download link
    },
    methods: {
        generateConfig() {
            console.log("Confirm button clicked");
            if (!this.datasetDescription || !this.selectedLibrary || !this.selectedView) {
                alert("Please fill in all the fields.");
                return;
            }

            const configData = {
                dataset_description: this.datasetDescription,
                library: this.selectedLibrary,
                view_type: this.selectedView
            };

            axios.post('/generate_config', configData)
            .then(response => {
                this.configOutput = JSON.stringify(response.data, null, 4);
                this.showModal = true; // Show the modal
            })
            .catch(error => {
                console.error('Error generating config:', error);
            });
        },

        closeModal() {
            this.showModal = false; // Close the modal
        },

        saveConfig() {
            const parsedConfig = JSON.parse(this.configOutput);
            axios.post('/save_config', {
                config_file: parsedConfig
            })
            .then(response => {
                alert('Config file saved successfully!');
                this.closeModal(); // Close the modal after saving
            })
            .catch(error => {
                console.error('Error saving config file:', error);
            });
        },

        downloadPrompts() {
            axios.post('/download_prompts', {
                dataset_description: this.datasetDescription,
                library: this.selectedLibrary,
                view_type: this.selectedView
            })
            .then(response => {
                const filename = response.headers['content-disposition'].split('filename=')[1].replace(/['"]/g, '');
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
            })
            .catch(error => {
                console.error('Error downloading prompts:', error);
            });
        },

        handleFileUpload(event) {
            this.selectedFile = event.target.files[0];
        },

        uploadFile() {
            if (!this.selectedFile) {
                alert('Please select a file to upload.');
                return;
            }

            let formData = new FormData();
            formData.append('file', this.selectedFile);
            console.log('Form data prepared:', this.selectedFile.name);
            axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                console.log('Upload response:', response.data);
                this.responseFileName = response.data.response_filename;
                this.responseDownloadLink = `/results/${this.responseFileName}`;
                alert('File processed successfully!');
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
        }
    }
});
