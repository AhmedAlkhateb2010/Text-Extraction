document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.getElementById('output').innerText = data.result;
        } else {
            document.getElementById('output').innerText = data.error || 'Error processing the file.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').innerText = 'An error occurred.';
    });
});
