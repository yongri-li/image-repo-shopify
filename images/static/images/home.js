

document.addEventListener('DOMContentLoaded', function () {
    //GET a list of images
    const repoList = document.querySelector('#repo-list')

    fetch(`/images/private`)
        .then(response => response.json())
        .then(repos => {
            console.log(repos)
            for (let i = 0; i < repos.length; i++) {
                let newContent = document.createElement('div');
                newContent.style.borderStyle = "groove"

                newContent.style.margin = "10px"
                let theImage = document.createElement('img');
                let title = document.createElement("h3");
                let des = document.createElement("p");

                title.innerHTML = repos[i].title;

                des.innerText = repos[i].description;

                theImage.setAttribute("src", repos[i].thumbnail);
                theImage.setAttribute("alt", repos[i].title);
                theImage.setAttribute("height", "100");

                newContent.append(title);
                newContent.append(theImage);
                newContent.append(des);
                newContent.addEventListener('click', () => {
                    console.log(`YOU JUST CLICKED ${repos[i].title} with the id of ${repos[i].id}`);
                    window.location.href = `/detail/${repos[i].id}`;
                })


                repoList.append(newContent);
            }
        })
})