function greetUser() {
    const messageElement = document.getElementById('message');
    messageElement.textContent = 'Hello! Welcome to our project!';
}

function openPdf(pdfUrl) {
    window.open(pdfUrl, '_blank');
}

function addVideos() {
    const videoElement = document.getElementById('video');
    const videoSetting = new Video();
    videoElement.textContent = `Added videos: ${videoSetting.toLocaleVideoString()}`;
}

function openVideoProcessing() {
    
}

function openImageProcessing() {
    
}

function openLiveProcessing() {
    
}

function openSettings() {
    
}

function openBacklog() {
    window.open('backlog.jpeg', '_blank');
}
