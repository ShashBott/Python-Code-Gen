document.getElementById('promptForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('promptInput').value;

    const response = await fetch('/generate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ prompt: prompt })
    });

    const data = await response.json();
    document.getElementById('output').textContent = data.generated_code;
});

// CSRF token helper function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log("CSRF Token:", cookieValue); // Log the CSRF token
    return cookieValue;
}
