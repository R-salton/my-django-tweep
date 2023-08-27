
    document.addEventListener('DOMContentLoaded', function() {
        const likeButtons = document.querySelectorAll('.like-button');
        likeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tweepId = this.getAttribute('data-tweep-id');
                likeTweep(tweepId);
            });
        });
    });

    function likeTweep(tweepId) {
        const csrfToken = '{{ csrf_token }}';
        fetch(`/api/tweep/${tweepId}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Display a message indicating success
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

