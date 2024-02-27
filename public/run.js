const menuDiv = '.MuiStack-root.css-1mzerio';
const links = [{ link: '/hello', text: 'Hello' }];
const timeOut = 300;


window.onload = function () {
    findNavandUpdate();
    addEventListenerToLinks();


}

function addEventListenerToLinks() {
    // Attach the event listener to the document
    document.addEventListener('click', function (e) {
        // Check if the clicked element is an 'a' tag
        if (e.target.tagName === 'A') {
            findNavandUpdate();
        }
    });
}

function findNavandUpdate() {
    var toolbarLinks = document.querySelector(menuDiv);
    console.log(toolbarLinks);
    if (toolbarLinks == null) {
        // Add a timeout to wait for the page to load
        setTimeout(function () {
            toolbarLinks = document.querySelector(menuDiv);

            if (toolbarLinks != null) {
                createButtons(toolbarLinks);
            };
        }, timeOut);
    } else {
        if (toolbarLinks != null) {
            createButtons(toolbarLinks);
        };
    }
}

function createButtons(toolbarLinks) {
    links.forEach(link => {
        if (document.getElementById(link.text) == null) {
            createButton(toolbarLinks, link.link, link.text);
        }
    });
}

function createButton(toolbarLinks, link, linkText) {
    var newLink = document.createElement('div');
    newLink.appendChild(document.createElement('span'));
    newLink.innerHTML = `<a class="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-disableElevation MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-disableElevation css-1v8u0lj" id="${linkText}" tabindex="0" href="${link}">${linkText}</a>`;
    toolbarLinks.appendChild(newLink);
}

