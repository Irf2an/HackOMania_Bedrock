let ingredientList = [];
let missingImages = [];
let ingredientImages = {}; // Store ingredient images

document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded");

    // ✅ Add event listener for the "View Favorites" button
    document.getElementById("favourites-btn").addEventListener("click", function () {
        loadFavoriteRecipes();
    });

    // ✅ Add event listener for the "Add Image" button
    document.getElementById("image-btn").addEventListener("click", function () {
        toggleSections("imageUploadSection");
    });

    // ✅ Add event listener for the "View Favorites" button
    document.getElementById("favourites-btn").addEventListener("click", function () {
        toggleSections("recipeResults");
        loadFavoriteRecipes(); // Load favorites when clicked
    });

});

// ✅ Function to toggle visibility of sections
function toggleSections(visibleSectionId) {
    let sections = ["imageUploadSection", "imagePreviewSection", "ingredientsDiv", "preferencesDiv", "recipeResults"];

    sections.forEach((sectionId) => {
        let section = document.getElementById(sectionId);
        if (section) {
            section.style.display = sectionId === visibleSectionId ? "block" : "none";
        }
    });

    console.log(`🔄 Switched to: ${visibleSectionId}`);
}

// ✅ Adds a new ingredient and fetches its image
function addIngredient() {
    let newIngredientInput = document.getElementById("newIngredient");
    let newIngredient = newIngredientInput.value.trim();

    if (!newIngredient) {
        alert("Please enter a valid ingredient.");
        return;
    }

    let cleanedIngredient = cleanIngredientName(newIngredient);

    if (ingredientList.includes(cleanedIngredient)) {
        alert("Ingredient already added.");
        return;
    }

    ingredientList.push(cleanedIngredient);

    // Try loading image from TheMealDB first
    let imgURL = `https://www.themealdb.com/images/ingredients/${cleanedIngredient}.png`;
    
    let imgLoad = new Image();
    imgLoad.src = imgURL;
    imgLoad.onload = function () {
        console.log(`✅ Image found for ${cleanedIngredient}: ${imgURL}`);
        ingredientImages[cleanedIngredient] = imgURL;
        displayIngredients();
    };
    
    imgLoad.onerror = function () {
        console.warn(`⚠️ Image not found for ${cleanedIngredient}, requesting from backend...`);
        fetchMissingIngredientImage(cleanedIngredient);
    };

    newIngredientInput.value = ""; // Clear input field after adding
}

// ✅ Fetch missing ingredient image from backend
function fetchMissingIngredientImage(ingredient) {
    fetch("/GPT/missing-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: [ingredient] })
    })
    .then(response => response.json())
    .then(data => {
        if (data[ingredient]) {
            console.log(`🟢 Missing image received for ${ingredient}: ${data[ingredient]}`);
            ingredientImages[ingredient] = data[ingredient]; // Store missing image
            
        } else {
            console.warn(`⚠️ No image found for ${ingredient}, using placeholder.`);
            ingredientImages[ingredient] = "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Fallback image
        }
        displayIngredients(); // ✅ Refresh UI after fetching image
        console.log("URL for " + ingredient + " = " + data[ingredient]);
        return data[ingredient];
    })
    .catch(error => {
        console.error(`🔴 Error fetching missing image for ${ingredient}:`, error);
        ingredientImages[ingredient] = "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Fallback image
        displayIngredients(); // Ensure UI updates even on failure
    });
}

// ✅ Fetch missing ingredient image from backend and return the image URL
async function fetchRecipeImage(ingredient) {
    try {
        let response = await fetch("/GPT/missing-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: [ingredient] })
        });

        let data = await response.json();

        if (data[ingredient]) {
            console.log(`🟢 Missing image received for ${ingredient}: ${data[ingredient]}`);
            return data[ingredient]; // ✅ Return the fetched image URL
        } else {
            console.warn(`⚠️ No image found for ${ingredient}, using placeholder.`);
            return "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Fallback image
        }
    } catch (error) {
        console.error(`🔴 Error fetching missing image for ${ingredient}:`, error);
        return "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Fallback image
    }
}


// Function to generate recipes with loading spinner
function generateRecipes() {
    let dietaryPref = document.getElementById("dietaryPref").value;
    let seasoningPref = document.getElementById("seasoningPref").value;
    let cookingTimePref = document.getElementById("cookingTimePref").value;
    let recipeStylePref = document.getElementById("recipeStylePref").value;
    let difficultyPref = document.getElementById("difficultyPref").value;
    let recipeContainer = document.getElementById("recipeResults");

    let userPreferences = {
        "Dietary Preference": dietaryPref,
        "Seasoning Preference": seasoningPref,
        "Cooking Time": cookingTimePref,
        "Recipe Style": recipeStylePref,
        "Difficulty Level": difficultyPref
    };

    let requestData = {
        ingredients: ingredientList,
        preferences: userPreferences
    };

    console.log("📡 Sending data to generate recipe:", requestData);

    // ✅ Show loading spinner
    showLoadingSpinner();

    fetch("/GPT/send-details", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ Recipe Response:", data);
        
        // Display recipes
        displayRecipe(data);

        // ✅ Hide spinner once the response is received
        hideLoadingSpinner();
    })
    .catch(error => {
        console.error("🔴 Error generating recipe:", error);
        
        // ✅ Hide spinner on error
        hideLoadingSpinner();

        // Show error message
        recipeContainer.innerHTML = "<p class='error-message'>⚠️ Error generating recipes. Please try again.</p>";
    });
}

// ✅ Function to show loading spinner
function showLoadingSpinner() {
    let recipeContainer = document.getElementById("recipeResults");
    recipeContainer.style.display = "block"; 
    recipeContainer.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Fetching delicious recipes... Please wait. 🍽️</p>
        </div>
    `;
}

// ✅ Function to hide loading spinner
function hideLoadingSpinner() {
    let recipeContainer = document.getElementById("recipeResults");
    recipeContainer.innerHTML = ""; // Clear spinner when recipes are loaded
}


// ✅ Fetch user's favorite recipes from backend
async function fetchFavoriteRecipes() {
    try {
        let response = await fetch("/favorites");
        let data = await response.json();
        return data.favorites || [];
    } catch (error) {
        console.error("Error fetching favorites:", error);
        return [];
    }
}

// ✅ Toggle favorite status and update class
function toggleFavorite(button, recipeName, ingredients, instructions) {
    let isFavorited = button.classList.contains("favorited");
    let action = isFavorited ? "unfavorite" : "favorite";

    fetch("/favorite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            recipe_name: recipeName,
            ingredients: ingredients,
            instructions: instructions,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);

        // ✅ Toggle class to change color (always keeps fa-heart)
        button.classList.toggle("favorited", !isFavorited);
    })
    .catch(error => console.error("Error:", error));
}


// ✅ Function to display recipes with correct heart status & share option
async function displayRecipe(recipeData) {
    console.log("recipeData = ", recipeData);
    let recipeContainer = document.getElementById("recipeResults");

    if (!recipeContainer) {
        console.error("❌ ERROR: recipeResults div not found!");
        return;
    }

    recipeContainer.style.display = "block";
    recipeContainer.innerHTML = "";

    let recipeTitle = document.createElement("h2");
    recipeTitle.innerHTML = "🍽️ <span>Recommended Recipes</span>";
    recipeTitle.classList.add("recipe-header");
    recipeContainer.appendChild(recipeTitle);

    let recipeList = document.createElement("div");
    recipeList.className = "recipe-grid";

    let recipes;
    try {
        recipes = JSON.parse(recipeData.recipes);
    } catch (error) {
        console.error("🚨 ERROR: Failed to parse recipes JSON!", error);
        recipeContainer.innerHTML = "<p class='error-message'>⚠️ Error processing recipes. Please try again.</p>";
        return;
    }

    if (!recipes || Object.keys(recipes).length === 0) {
        recipeContainer.innerHTML = "<p class='error-message'>⚠️ No recipes generated. Try again!</p>";
        return;
    }

    // ✅ Fetch user's favorite recipes before rendering
    let favoriteRecipes = await fetchFavoriteRecipes();

    let recipeCardsPromises = Object.values(recipes).map(async (recipe) => {
        if (!recipe || !recipe["Dish Name"]) {
            console.warn("⚠️ Skipping invalid recipe:", recipe);
            return null;
        }

        let recipeCard = document.createElement("div");
        recipeCard.className = "recipe-card";

        let dishName = document.createElement("h3");
        dishName.innerText = recipe["Dish Name"];
        recipeCard.appendChild(dishName);

        let recipeImage = document.createElement("img");
        recipeImage.className = "recipe-img";
        recipeImage.src = await fetchRecipeImage(recipe["Dish Name"]);
        recipeCard.appendChild(recipeImage);

        // ✅ Create Heart Button using Font Awesome
        let favoriteButton = document.createElement("button");
        favoriteButton.className = "fa fa-heart favorite-btn"; // Default: empty heart
        favoriteButton.setAttribute("data-recipe-name", recipe["Dish Name"]);

        // ✅ Check if recipe is in favorites and update class
        if (favoriteRecipes.some(fav => fav.recipe_name === recipe["Dish Name"])) {
            favoriteButton.classList.add("fa-heart"); // Full heart if favorited
            favoriteButton.classList.add("favorited");
        }

        favoriteButton.addEventListener("click", function () {
            toggleFavorite(favoriteButton, recipe["Dish Name"], recipe["Ingredients"], recipe["Instructions"]);
        });

        recipeCard.appendChild(favoriteButton);

        // ✅ Create Share Button
        let shareButton = document.createElement("button");
        shareButton.classList.add("share-btn");
        shareButton.innerHTML = `<i class="fa fa-share"></i> Share`; // Adds a nice icon
        shareButton.addEventListener("click", function () {
            openShareModal(recipe["Dish Name"], recipe["Ingredients"], recipe["Instructions"]);
        });

        recipeCard.appendChild(shareButton);


        if (Array.isArray(recipe["Ingredients"])) {
            let ingredientsBox = document.createElement("div");
            ingredientsBox.className = "ingredients-box";

            let ingredientsTitle = document.createElement("h4");
            ingredientsTitle.innerText = "🛒 Ingredients";
            ingredientsBox.appendChild(ingredientsTitle);

            let ingredientsList = document.createElement("ul");
            recipe["Ingredients"].forEach((ingredient) => {
                let li = document.createElement("li");
                li.innerText = capitalizeWords(ingredient);
                ingredientsList.appendChild(li);
            });

            ingredientsBox.appendChild(ingredientsList);
            recipeCard.appendChild(ingredientsBox);
        }

        if (Array.isArray(recipe["Instructions"])) {
            let instructionsBox = document.createElement("div");
            instructionsBox.className = "instructions-box";

            let instructionsTitle = document.createElement("h4");
            instructionsTitle.innerText = "📝 Instructions";
            instructionsBox.appendChild(instructionsTitle);

            let instructionsList = document.createElement("ol");
            recipe["Instructions"].forEach((step) => {
                let li = document.createElement("li");
                li.innerHTML = removeStepNumbering(step);
                instructionsList.appendChild(li);
            });

            instructionsBox.appendChild(instructionsList);
            recipeCard.appendChild(instructionsBox);
        }

        return recipeCard;
    });

    let recipeCards = await Promise.all(recipeCardsPromises);
    recipeCards.forEach((card) => {
        if (card) recipeList.appendChild(card);
    });

    recipeContainer.appendChild(recipeList);
}


// ✅ Function to capitalize ingredients
function capitalizeWords(str) {
    return str
        .split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

// ✅ Function to remove "Step X:" from instructions
function removeStepNumbering(stepText) {
    return stepText.replace(/Step \d+:\s?/i, ""); // Removes "Step X:" at the beginning
}


// Helper function to format recipe output
function formatRecipeOutput(recipeText) {
    return recipeText
        .replace(/\n\n/g, "<br><br>") // Preserve paragraph spacing
        .replace(/\n- /g, "<br>🔸 ") // Bullet points for ingredients
        .replace(/\n[0-9]+\./g, match => `<br><strong>${match.trim()}</strong>`); // Step numbers bold
}


document.getElementById("image-btn").addEventListener("click", function () {
    let uploadSection = document.getElementById("imageUploadSection");

    // Toggle visibility
    if (uploadSection.style.display === "none" || uploadSection.style.display === "") {
        uploadSection.style.display = "block";
    } else {
        uploadSection.style.display = "none";
    }
});

// Function to preview the image before uploading
function previewImage(event) {
    let reader = new FileReader();
    reader.onload = function () {
        let preview = document.getElementById("preview");
        let identifyBtn = document.getElementById("identifyBtn");
        let previewSection = document.getElementById("imagePreviewSection");

        preview.src = reader.result;
        preview.style.display = "block"; // Show the preview image
        identifyBtn.style.display = "block"; // Show the identify button
        previewSection.style.display = "flex"; // Show preview section
    };
    reader.readAsDataURL(event.target.files[0]);
}

document.querySelector(".preferences-container button").addEventListener("click", function() {
    this.style.transform = "scale(1.1)";
    setTimeout(() => {
        this.style.transform = "scale(1)";
    }, 150);
});

function uploadImage() {
    let fileInput = document.getElementById("imageUpload");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);
    
    console.log("Fetching...");

    // ✅ Show loading spinner before sending request
    showLoadingSpinnerForIngredients();

    fetch("/GPT/send-image", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.ingredients) {
            ingredientList = data.ingredients.map(cleanIngredientName);
            missingImages = [];
            fetchAndDisplayAllImages(); // Fetch images first before displaying
        } else {
            alert("No ingredients detected.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        hideLoadingSpinnerForIngredients();
    });
}

// ✅ Function to show loading spinner for identifying ingredients
function showLoadingSpinnerForIngredients() {
    let ingredientsContainer = document.getElementById("ingredientsSpinnerDiv");
    ingredientsContainer.style.display = "block";
    ingredientsContainer.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Identifying ingredients... Please wait. 🥦🍅</p>
        </div>
    `;
}

// ✅ Function to hide loading spinner after identifying ingredients
function hideLoadingSpinnerForIngredients() {
    let ingredientsContainer = document.getElementById("ingredientsSpinnerDiv");
    ingredientsContainer.innerHTML = ""; // Remove spinner when ingredients are loaded
}

// ✅ Fetch both local and missing images first, then display the UI
function fetchAndDisplayAllImages() {
    let imageLoadPromises = [];
    missingImages = [];

    console.log("🟡 Fetching all ingredient images...");

    ingredientList.forEach((ingredient) => {
        let cleanedName = cleanIngredientName(ingredient);
        let imgURL = `https://www.themealdb.com/images/ingredients/${cleanedName}.png`;

        let imgLoad = new Promise((resolve) => {
            let img = new Image();
            img.src = imgURL;
            img.onload = () => {
                ingredientImages[cleanedName.toLowerCase()] = imgURL; // Store in lowercase for consistency
                resolve();
            };
            img.onerror = () => {
                missingImages.push(cleanedName); // Add to missing list
                resolve();
            };
        });

        imageLoadPromises.push(imgLoad);
    });

    // ✅ Wait for all image loads
    Promise.all(imageLoadPromises).then(() => {
        console.log("🟠 Missing images list:", missingImages);
        if (missingImages.length > 0) {
            fetchMissingImages(missingImages);
        } else {
            displayIngredients(); // Show ingredients if no missing images
        }
    });
}

// ✅ Fetch missing images from the backend
function fetchMissingImages(missingList) {
    console.log("🔵 Sending missing ingredients request:", JSON.stringify({ missing_ingredients: missingList }));

    fetch("/GPT/missing-url", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: missingList })
    })
    .then(response => response.json())
    .then(data => {
        console.log("🟢 Received missing image data from backend:", data);

        Object.keys(data).forEach((ingredient) => {
            let cleanedKey = cleanIngredientName(ingredient).toLowerCase();
            ingredientImages[cleanedKey] = data[ingredient]; // Store updated image URL
        });

        displayIngredients(); // ✅ Now display all ingredients
    })
    .catch(error => {
        console.error("🔴 Error fetching missing images:", error);
        displayIngredients(); // Proceed even if fetching fails
    });
}

// ✅ Function to display ingredients AFTER all images are loaded
function displayIngredients() {
    let grid = document.getElementById("ingredientsGrid");
    grid.innerHTML = ""; // Clear existing content

    if (ingredientList.length === 0) {
        console.error("⚠️ No ingredients to display.");
        return;
    }

    ingredientList.forEach((ingredient, index) => {
        let cleanedName = cleanIngredientName(ingredient).toLowerCase();
        let imageUrl = ingredientImages[cleanedName];
        let card = document.createElement("div");
        card.className = "ingredient-card";

        // Image Element
        let img = document.createElement("img");
        img.src = imageUrl;
        img.className = "ingredient-img";

        // Input + Delete Button Container
        let inputContainer = document.createElement("div");
        inputContainer.className = "input-delete-container";

        // Input Field for Editing
        let input = document.createElement("input");
        input.type = "text";
        input.value = capitalizeWords(cleanedName);
        input.className = "ingredient-input";
        input.onchange = function () {
            console.log(`📝 Ingredient changed: ${cleanedName} → ${this.value}`);
            updateIngredient(index, this.value);
        };

        // Delete Button
        let deleteBtn = document.createElement("button");
        deleteBtn.innerHTML = "❌";
        deleteBtn.className = "delete-btn";
        deleteBtn.onclick = function () {
            console.log(`❌ Deleting ingredient: ${cleanedName}`);
            deleteIngredient(index);
        };

        // Append elements
        inputContainer.appendChild(input);
        inputContainer.appendChild(deleteBtn);
        card.appendChild(img);
        card.appendChild(inputContainer);
        grid.appendChild(card);
    });
    document.getElementById("ingredientsDiv").style.display = "block";
    document.getElementById("preferencesDiv").style.display = "block";
    hideLoadingSpinnerForIngredients(); // ✅ Hide spinner after display
}

// ✅ Function to clean ingredient names
function cleanIngredientName(name) {
    return name.trim().replace(/\.$/, "").toLowerCase();
}

// ✅ Function to capitalize words properly
function capitalizeWords(str) {
    return str.split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

// ✅ Function to update an ingredient
function updateIngredient(index, newValue) {
    let cleanedValue = cleanIngredientName(newValue);

    if (!cleanedValue) {
        alert("Please enter a valid ingredient.");
        return;
    }

    if (ingredientList.includes(cleanedValue)) {
        alert("Ingredient already exists.");
        return;
    }

    console.log(`📝 Updating ${ingredientList[index]} to ${cleanedValue}`);

    // Update the ingredient list
    ingredientList[index] = cleanedValue;

    // Try fetching the image from TheMealDB first
    let imgURL = `https://www.themealdb.com/images/ingredients/${cleanedValue}.png`;

    let imgLoad = new Image();
    imgLoad.src = imgURL;
    imgLoad.onload = function () {
        console.log(`✅ Image found for ${cleanedValue}: ${imgURL}`);
        ingredientImages[cleanedValue] = imgURL;
        displayIngredients();
    };
    
    imgLoad.onerror = function () {
        console.warn(`⚠️ Image not found for ${cleanedValue}, requesting from backend...`);
        fetchMissingIngredientImage(cleanedValue);
    };
}

// ✅ Function to delete an ingredient with confirmation
function deleteIngredient(index) {
    let ingredientName = ingredientList[index];

    // Show confirmation dialog
    let confirmDelete = confirm(`Are you sure you want to delete "${ingredientName}"?`);
    if (!confirmDelete) {
        console.log(`❌ Deletion cancelled for ${ingredientName}`);
        return; // Stop function if user cancels
    }

    console.log(`❌ Deleting ${ingredientName}`);

    // Remove from ingredientList
    ingredientList.splice(index, 1);

    // Remove from ingredientImages if exists
    delete ingredientImages[ingredientName];

    // Directly remove the ingredient card from the UI
    let grid = document.getElementById("ingredientsGrid");
    let cards = grid.getElementsByClassName("ingredient-card");

    if (cards[index]) {
        cards[index].remove();
        console.log(`✅ Removed ${ingredientName} from UI`);
    } else {
        console.warn(`⚠️ Could not find UI element for ${ingredientName}`);
    }
}

// ✅ Fetch and display favorite recipes
async function loadFavoriteRecipes() {
    console.log("Fetching favorite recipes...");

    // ✅ Show loading spinner
    showFavoritesSpinner();

    try {
        let response = await fetch("/favorites"); // API call to get favorite recipes
        let data = await response.json();

        if (!data.favorites || data.favorites.length === 0) {
            document.getElementById("recipeResults").innerHTML = "<p class='error-message'>⚠️ No favorite recipes found.</p>";
            return;
        }

        console.log("Favorite Recipes:", data.favorites);
        displayFavorites(data.favorites); // Call function to display favorites

        // ✅ Hide spinner once the response is received
        hideFavoritesSpinner();
    } catch (error) {
        console.error("Error fetching favorites:", error);

        // ✅ Hide spinner on error
        hideFavoritesSpinner();

        document.getElementById("recipeResults").innerHTML = "<p class='error-message'>⚠️ Error loading favorites.</p>";
    }
}

// ✅ Function to show the spinner
function showFavoritesSpinner() {
    let spinnerDiv = document.getElementById("favoritesSpinnerDiv");
    spinnerDiv.style.display = "block"; // Show spinner
}

// ✅ Function to hide the spinner
function hideFavoritesSpinner() {
    let spinnerDiv = document.getElementById("favoritesSpinnerDiv");
    spinnerDiv.style.display = "none"; // Hide spinner
}


// ✅ Display favorite recipes (similar to displayRecipe)
function displayFavorites(favorites) {
    let recipeContainer = document.getElementById("recipeResults");

    if (!recipeContainer) {
        console.error("❌ ERROR: recipeResults div not found!");
        return;
    }

    recipeContainer.style.display = "block";
    recipeContainer.innerHTML = ""; // Clear previous content

    let recipeTitle = document.createElement("h2");
    recipeTitle.innerHTML = "⭐ <span>Your Favorite Recipes</span>";
    recipeTitle.classList.add("recipe-header");
    recipeContainer.appendChild(recipeTitle);

    let recipeList = document.createElement("div");
    recipeList.className = "recipe-grid";

    let recipeCardsPromises = favorites.map(async (recipe) => {
        if (!recipe || !recipe.recipe_name) {
            console.warn("⚠️ Skipping invalid favorite recipe:", recipe);
            return null;
        }

        let recipeCard = document.createElement("div");
        recipeCard.className = "recipe-card";

        let dishName = document.createElement("h3");
        dishName.innerText = recipe.recipe_name;
        recipeCard.appendChild(dishName);

        let recipeImage = document.createElement("img");
        recipeImage.className = "recipe-img";
        recipeImage.src = await fetchRecipeImage(recipe.recipe_name);
        recipeCard.appendChild(recipeImage);

        // ✅ Create Favorite Button using Font Awesome
        let favoriteButton = document.createElement("button");
        favoriteButton.classList.add("fa", "fa-heart", "favorite-btn", "favorited"); // Always favorited
        favoriteButton.setAttribute("data-recipe-name", recipe.recipe_name);

        favoriteButton.addEventListener("click", function () {
            toggleFavorite(favoriteButton, recipe.recipe_name, recipe.ingredients, recipe.instructions);
        });

        recipeCard.appendChild(favoriteButton);

        // ✅ Create Share Button
        let shareButton = document.createElement("button");
        shareButton.classList.add("share-btn");
        shareButton.innerHTML = `<i class="fa fa-share"></i> Share`; // Adds icon
        shareButton.addEventListener("click", function () {
            openShareModal(recipe.recipe_name, recipe.ingredients, recipe.instructions);
        });

        recipeCard.appendChild(shareButton);

        if (Array.isArray(recipe.ingredients)) {
            let ingredientsBox = document.createElement("div");
            ingredientsBox.className = "ingredients-box";

            let ingredientsTitle = document.createElement("h4");
            ingredientsTitle.innerText = "🛒 Ingredients";
            ingredientsBox.appendChild(ingredientsTitle);

            let ingredientsList = document.createElement("ul");
            recipe.ingredients.forEach((ingredient) => {
                let li = document.createElement("li");
                li.innerText = capitalizeWords(ingredient);
                ingredientsList.appendChild(li);
            });

            ingredientsBox.appendChild(ingredientsList);
            recipeCard.appendChild(ingredientsBox);
        }

        if (Array.isArray(recipe.instructions)) {
            let instructionsBox = document.createElement("div");
            instructionsBox.className = "instructions-box";

            let instructionsTitle = document.createElement("h4");
            instructionsTitle.innerText = "📝 Instructions";
            instructionsBox.appendChild(instructionsTitle);

            let instructionsList = document.createElement("ol");
            recipe.instructions.forEach((step) => {
                let li = document.createElement("li");
                li.innerHTML = removeStepNumbering(step);
                instructionsList.appendChild(li);
            });

            instructionsBox.appendChild(instructionsList);
            recipeCard.appendChild(instructionsBox);
        }

        return recipeCard;
    });

    Promise.all(recipeCardsPromises).then((recipeCards) => {
        recipeCards.forEach((card) => {
            if (card) recipeList.appendChild(card);
        });
        recipeContainer.appendChild(recipeList);
    });
}

// ✅ Open Share Modal with Custom Message
function openShareModal(recipeName, ingredients, instructions) {
    let modal = document.getElementById("shareModal");
    modal.style.display = "flex"; // Show modal

    let defaultMessage = `🍽️ Check out this recipe: ${recipeName}!  
Ingredients: ${ingredients.join(", ")}  
Steps: ${instructions.join(". ")}`;

    document.getElementById("customMessage").value = defaultMessage;

    // ✅ Set up sharing buttons
    document.getElementById("shareTwitter").onclick = function () {
        shareOnSocial("twitter");
    };
    document.getElementById("shareFacebook").onclick = function () {
        shareOnSocial("facebook");
    };
    document.getElementById("shareWhatsApp").onclick = function () {
        shareOnSocial("whatsapp");
    };
}

// ✅ Close the Modal
function closeShareModal() {
    document.getElementById("shareModal").style.display = "none";
}

// ✅ Share on Selected Social Platform
function shareOnSocial(platform) {
    let message = encodeURIComponent(document.getElementById("customMessage").value);
    let url = "https://tinyurl.com/bedrock-hackomania"; // Change this to actual app URL

    let shareUrl = "";
    if (platform === "twitter") {
        shareUrl = `https://twitter.com/intent/tweet?text=${message}&url=${url}`;
    } else if (platform === "facebook") {
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}&quote=${message}`;
    } else if (platform === "whatsapp") {
        shareUrl = `https://api.whatsapp.com/send?text=${message} ${url}`;
    }

    window.open(shareUrl, "_blank");
}
