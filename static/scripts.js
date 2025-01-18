document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const output = document.getElementById('output');
        if (data.download_link) {
            output.innerHTML = `
                <p>File processed successfully! You can <a href="${data.download_link}" download>download it now</a>.</p>
            `;
        } else {
            output.innerHTML = `<p style="color: red;">${data.error || 'Error processing the file.'}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').innerHTML = '<p style="color: red;">An error occurred.</p>';
    });
});
