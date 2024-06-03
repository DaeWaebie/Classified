  document.addEventListener('DOMContentLoaded', () => {
    const dragArea = document.querySelector('.drag-drop-area');
    const fileInput = document.getElementById('file');
    const uploadText = document.getElementById('uploadText');

    if (dragArea) {
        dragArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dragArea.classList.add('drag-over');
        });

        dragArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dragArea.classList.remove('drag-over');
        });

        dragArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dragArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            handleFiles(files);
            displayFileNames(files);
        });

        dragArea.addEventListener('click', (e) => {
            if (e.target === dragArea || e.target === uploadText) {
                fileInput.click();
            }
        });
    }

    fileInput.addEventListener('change', (event) => {
        const files = event.target.files;
        handleFiles(files);
        displayFileNames(files);
    });

    function handleFiles(files) {
        for (const file of files) {
            if (file.type !== 'video/mp4') {
                alert('MP4 파일만 업로드 가능합니다.');
                return;
            }
        }
    }

    function displayFileNames(files) {
        let fileNames = [];
        for (const file of files) {
            fileNames.push(file.name);
        }
        if (fileNames.length > 0) {
            uploadText.innerHTML = fileNames.join('<br>');
        } else {
            uploadText.innerHTML = 'Try again';
        }
    }
});


