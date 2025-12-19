document.addEventListener('DOMContentLoaded', () => {
    const favBtn = document.getElementById('favoriteBtn');
    const starIcon = document.getElementById('starIcon');

    if (favBtn && starIcon) {
        favBtn.addEventListener('click', function() {
            starIcon.classList.toggle('fa-regular');
            starIcon.classList.toggle('fa-solid');

            starIcon.classList.toggle('text-white');
            starIcon.classList.toggle('text-yellow-400');
            
            console.log("Favorite status toggled!");
        });
    }
});