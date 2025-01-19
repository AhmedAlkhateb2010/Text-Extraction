/* File path: C:\Users\Msi\Desktop\Text Extraction\static\script.js */

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    // Change button text and disable it while processing
    const convertButton = document.getElementById('convert-button');
    convertButton.innerText = 'Processing...';
    convertButton.disabled = true;

    // Send the file to the server
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const output = document.getElementById('output');
        if (data.download_link) {
            // Display download link on success
            output.innerHTML = `
                <p>File processed successfully! You can <a href="${data.download_link}" download>download it now</a>.</p>
            `;
        } else {
            // Show error message if processing failed
            output.innerHTML = `<p style="color: red;">${data.error || 'Error processing the file.'}</p>`;
        }
        
        // Reset the button
        convertButton.innerText = 'Convert to Text';
        convertButton.disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').innerHTML = '<p style="color: red;">An error occurred.</p>';
        
        // Reset the button
        convertButton.innerText = 'Convert to Text';
        convertButton.disabled = false;
    });
});
