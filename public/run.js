function openNav() {
    document.getElementById("myNav").style.width = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}

function addTheMenu(addMenuToFn) {
    const header = document.querySelector('header');
    if (header) {
        addMenuToFn(header.nextElementSibling);
    } else {
        setTimeout(() => {
            addTheMenu(addMenuToFn);
        }, 200);
    }
}

function addMenuTo(element) {
    if (document.getElementById("myNav")) {
        return;
    }
    menuHtml =
        `<div id="myNav" class="overlay">

        <!-- Button to close the overlay navigation -->
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
    
        <!-- Overlay content -->
        <div class="overlay-content">
        <a href="/hello">About</a>
        <a href="#">Services</a>
        <a href="#">Clients</a>
        <a href="#">Contact</a>
        </div>
    
    </div>`;
    buttonHtml = `<span onclick="openNav()" class="menuBtn">☰ open</span>`;
    element.insertAdjacentHTML('beforebegin', buttonHtml);
    element.insertAdjacentHTML('beforebegin', menuHtml);
}


// window.onload = function () {
//     // addTheMenu(addMenuTo);

//     var observer = new MutationObserver(function (mutations) {
//         // Run your function
//         addTheMenu(addMenuTo);
//     });

//     // Configuration of the observer:
//     var config = { attributes: true, childList: true, subtree: true };

//     // Pass in the target node (body), as well as the observer options
//     observer.observe(document.body, config);

// }



