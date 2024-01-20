const mealPlanner = document.querySelector('.calendar')
const mealPlannerEventListener = mealPlanner.addEventListener('click', handleClick)

const form = document.querySelector('.meal-form')
const recipeDetails = document.querySelector('.recipe-detail')
const initialRender = document.querySelector('.initial')

function init(){
    initialRender.style.display = 'block'
    recipeDetails.style.display = 'none';
    form.style.display = 'none'
}

function handleClick(e){
    e.preventDefault()
    if (e.target.classList.contains('no-meal')) {
        let mealType = e.target.attributes['meal-type'].value
        let date = e.target.attributes['meal-date'].value
        let collabGroup = e.target.attributes['collab-group'].value

        showMealForm(mealType, date, collabGroup);
    }
    
    if (e.target.classList.contains('scheduled-meal')) {
        let recipe = e.target.attributes['recipe'].value
        let recipeId = e.target.attributes['recipe-id'].value
        let collabGroup = e.target.attributes['collab-group'].value
        console.log(recipeId)

        let ingredients = e.target.attributes['ingredients'].value
        let ingredientArray = ingredients.split('\n')
        console.log(ingredientArray)
        let ingredientList = ingredientArray.map(ingredient => `<li>${ingredient}</li>`).join('')

        let instructions = e.target.attributes['instructions'].value
        let instructionArray = instructions.split('\n')
        let instructionList = instructionArray.map(instruction => `<li>${instruction}</li>`).join('')

        displayMealDetails(recipe, ingredientList, instructionList, recipeId, collabGroup)
    }
}

function showMealForm(type, date, group) {
    form.style.display = 'block'
    initialRender.style.display = 'none'
    recipeDetails.style.display = 'none'

    const typeInput = form.querySelector('input[name="type"]')
    const dateInput = form.querySelector('input[name="date"]')
    const groupInput = form.querySelector('input[name="collab_group"]')

    typeInput.value = type;
    dateInput.value = date;
    groupInput.value = group;
}

function displayMealDetails(recipe, ingredients, instructions, id, group) {

    recipeDetails.style.display = 'block';
    form.style.display = 'none'
    initialRender.style.display = 'none'
    console.log('before details')

    recipeDetails.innerHTML = `<h2>${recipe}</h2>
    <a href="/groups/${group}/recipes/${id}">Recipe detail page</a>
    <h4>Ingredients</h4>
    <ul>${ingredients}</ul>
    <h4>Instructions</h4>
    <ol>${instructions}</ol>
    `
}

init()