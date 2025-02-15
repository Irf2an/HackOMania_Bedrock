let ingredientList = [];
let missingImages = [];
let ingredientImages = {}; // Store ingredient images

document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded");
});

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
        
        // ✅ Hide spinner once the response is received
        hideLoadingSpinner();
        
        // Display recipes
        displayRecipe(data);
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


async function displayRecipe(recipeData) {
    console.log("recipeData = ", recipeData);
    let recipeContainer = document.getElementById("recipeResults");

    if (!recipeContainer) {
        console.error("❌ ERROR: recipeResults div not found!");
        return;
    }

    // Show the recipe container when data is available
    recipeContainer.style.display = "block";
    recipeContainer.innerHTML = ""; // Clear previous content

    // Recipe Title
    let recipeTitle = document.createElement("h2");
    recipeTitle.innerHTML = "🍽️ <span>Recommended Recipes</span>";
    recipeTitle.classList.add("recipe-header");
    recipeContainer.appendChild(recipeTitle);

    // Create recipe grid container
    let recipeList = document.createElement("div");
    recipeList.className = "recipe-grid";

    // ✅ Parse the JSON string from API
    let recipes;
    try {
        recipes = JSON.parse(recipeData.recipes);
    } catch (error) {
        console.error("🚨 ERROR: Failed to parse recipes JSON!", error);
        recipeContainer.innerHTML = "<p class='error-message'>⚠️ Error processing recipes. Please try again.</p>";
        return;
    }

    if (!recipes || Object.keys(recipes).length === 0) {
        console.error("🚨 ERROR: No valid recipes found in response", recipes);
        recipeContainer.innerHTML = "<p class='error-message'>⚠️ No recipes generated. Try again!</p>";
        return;
    }

    // ✅ Fetch all images before rendering UI
    let recipeCardsPromises = Object.values(recipes).map(async (recipe) => {
        if (!recipe || !recipe["Dish Name"]) {
            console.warn("⚠️ Skipping invalid recipe:", recipe);
            return null;
        }

        let recipeCard = document.createElement("div");
        recipeCard.className = "recipe-card";

        // Dish Name
        let dishName = document.createElement("h3");
        dishName.innerText = recipe["Dish Name"];
        recipeCard.appendChild(dishName);

        // ✅ Create placeholder image first
        let recipeImage = document.createElement("img");
        recipeImage.className = "recipe-img";
        recipeImage.src = "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Default while loading
        recipeCard.appendChild(recipeImage);

        // ✅ Fetch image asynchronously and update the image source
        let imageUrl = await fetchRecipeImage(recipe["Dish Name"]);
        console.log(`✅ Image URL received for ${recipe["Dish Name"]}: ${imageUrl}`);
        recipeImage.src = imageUrl || "https://cdn-icons-png.flaticon.com/128/4461/4461744.png"; // Update image

        // Ingredients List
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

        // Instructions List
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

        return recipeCard; // Return the completed recipe card
    });

    // ✅ Wait for all images before displaying recipes
    let recipeCards = await Promise.all(recipeCardsPromises);

    // Append each completed card to the grid
    recipeCards.forEach((card) => {
        if (card) recipeList.appendChild(card);
    });

    // Append the grid to the container
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

