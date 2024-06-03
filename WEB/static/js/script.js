const dragArea = document.querySelector('.drag-drop-area');
const fileInput = document.getElementById('fileInput');
const dragText = document.querySelector('.header');
const uploadText = document.getElementById('uploadText'); // 추가: 업로드 텍스트를 표시할 요소

let button = document.querySelector('.button');
let input = document.querySelector('input');

function dragOverHandler(event) {
    event.preventDefault();
    dragArea.classList.add('drag-over');
}

function dropHandler(event) {
    event.preventDefault();
    dragArea.classList.remove('drag-over');
    const files = event.dataTransfer.files;
    handleFiles(files);
    displayFileNames(files); // 추가: 파일명을 표시하는 함수 호출
}

function handleFiles(files) {
    for (const file of files) {
        if (file.type !== 'video/mp4') {
            alert('Only mp4 files can be uploaded');
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
        uploadText.innerHTML = 'Click or Drag files here to upload videos';
    }
}

dragArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFiles(files);
    displayFileNames(files); // 추가: 파일명을 표시하는 함수 호출
});

let file;
button.onclick = () => {
    input.click();
};

input.addEventListener('change', function () {
    file = this.files[0];
    dragArea.classList.add('active');
    displayFile();
});

function displayFile() {
    let fileType = file.type;
    let validExtensions = ['video/mp4'];
    if (validExtensions.includes(fileType)) {
        let fileReader = new FileReader();
        fileReader.onload = () => {
            let fileURL = fileReader.result;
        };
        fileReader.readAsDataURL(file);
    } else {
        alert('지원되는 형식의 파일이 아닙니다!');
        dragArea.classList.remove('active');
    }
}

   
