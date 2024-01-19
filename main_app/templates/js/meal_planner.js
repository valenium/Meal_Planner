const mealPlanner = document.querySelector('.meal-planner-container')
const mealPlannerEventListener = mealPlanner.addEventListener('click', handleClick)

const form = document.querySelector('meal-form')
const recipeDetails = document.querySelector('.recipe-detail-view')
const initialRender = document.querySelector('.initial')

document.addEventListener('DOMContentLoaded', function () {
    mealPlanner.addEventListener('click', function (e) {
        // If "No meal assigned" is clicked, show the form
        if (e.target.classList.contains('no-meal')) {
            let mealType = e.target.closest('.meal-slot').dataset.type;
            let date = e.target.closest('.meal-slot').dataset.date;
            showMealForm(mealType, date);
        }
        
        if (e.target.classList.contains('meal-name')) {
            let recipeId = e.target.dataset.recipeId;
            displayMealDetails(recipeId);
        }
    });
});

function init(){
    initialRender.style.display = 'block'
}

function handleClick(e){
    if (e.target.classList.contains('no-meal')) {
        let mealType = e.target.closest('.meal-slot').dataset.type;
        let date = e.target.closest('.meal-slot').dataset.date;
        showMealForm(mealType, date);
    }
    
    if (e.target.classList.contains('meal-name')) {
        let recipeId = e.target.dataset.recipeId;
        displayMealDetails(recipeId);
    }
}

function showMealForm() {
    form.style.display = 'block'
    initialRender.style.display = 'none'
    recipeDetails.style.display = 'none'
}

function displayMealDetails(recipeId) {
    // Fetch and display details for the selected meal
    // This might involve an AJAX request to get the details and then displaying them
    let detailsContainer = document.getElementById('selected-meal-details');
    detailsContainer.innerHTML = '<p>Loading...</p>';
    detailsContainer.style.display = 'block';
    
    // Example AJAX request (You'll need to set up a URL endpoint to handle this)
    fetch(`/path_to_your_endpoint/?recipeId=${recipeId}`)
        .then(response => response.json())
        .then(data => {
            // Assuming 'data' contains the meal details
            detailsContainer.innerHTML = `<p>${data.title}</p>`;
        })
        .catch(error => {
            detailsContainer.innerHTML = '<p>Error loading details.</p>';
        });
}

init()