let stars = document.querySelectorAll('.star');
stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        let phoneId = star.dataset.phoneId;
        fetch('/rate_phone/', {
            method: 'POST',
            body: JSON.stringify({
                'phone_id': phoneId,
                'stars': index + 1
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status == 'ok') {
                // Rating was successful
                alert('Thanks for your rating!');
                // Also, let's update the stars visually
                for (let j = 0; j <= index; j++) {
                    stars[j].innerHTML = '&#9733;';
                }
            }
        });
    });
});