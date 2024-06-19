document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const form = document.getElementById('upload-form');

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('hover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('hover');
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('hover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileList(files);
        }
    });

    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            updateFileList(fileInput.files);
        }
    });

    form.addEventListener('submit', (event) => {
        if (fileInput.files.length === 0) {
            event.preventDefault();
            alert('Proszę wybrać plik przed przesłaniem.');
        }
    });

    function updateFileList(files) {
        fileList.innerHTML = '';
        for (let i = 0; i < files.length; i++) {
            const li = document.createElement('li');
            li.textContent = files[i].name;
            fileList.appendChild(li);
        }
    }
});