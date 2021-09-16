

document.addEventListener('DOMContentLoaded', function() {
    //GET a list of images
    const imageList = document.querySelector('#image-list')

    fetch(`/images/private`)
    .then(response => response.json())
    .then(images => {
        console.log(images)
        for (let i =0;i<images.length;i++) {
            let newContent = document.createElement('div');
            newContent.style.borderStyle = "groove"
            let theImage = document.createElement('img');
            let title = document.createElement("p");

            title.innerHTML = images[i].title
            newContent.append(title)
            theImage.setAttribute("src",images[i].image);
            theImage.setAttribute("alt",images[i].title)
            theImage.setAttribute("height","100")

            newContent.append(theImage)
            imageList.append(newContent)
        }
    })
})