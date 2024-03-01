function openNav() {
    document.getElementById("myNav").style.width = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}

function getFirstElement() {
    return document.querySelector('header').nextElementSibling;
}


window.onload = function () {

    var firstElement = getFirstElement();
    console.log(firstElement);
    // Take this html smippet and add it to the page
    menuHtml =
        `<div id="myNav" class="overlay">

            <!-- Button to close the overlay navigation -->
            <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        
            <!-- Overlay content -->
            <div class="overlay-content">
            <a href="#">About</a>
            <a href="#">Services</a>
            <a href="#">Clients</a>
            <a href="#">Contact</a>
            </div>
        
        </div>`;
    buttonHtml = `<span onclick="openNav()" class="menuBtn">☰ open</span>`;
    firstElement.insertAdjacentHTML('beforebegin', buttonHtml);
    firstElement.insertAdjacentHTML('beforebegin', menuHtml);
}

