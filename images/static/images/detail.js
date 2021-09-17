

console.log("HELLO")
document.addEventListener('DOMContentLoaded', function () {

    const repo = document.querySelector('#repo-detail')
    const repoID = document.URL.split("/")[document.URL.split("/").length - 1]

    fetch(`/repo_details/${repoID}`)
        .then(response => response.json())
        .then(details => {
            console.log(details);
            let title = document.createElement("h2");
            let user = document.createElement("h5");
            let selected = document.createElement("button");
            selected.addEventListener('click', function () {
                console.log("BUTTON PRESSED");
                checks = document.querySelectorAll("input");
                console.log(checks)
                for (let i = 0; i < checks.length; i++) {
                    console.log(checks[i])
                }

            })


            selected.innerHTML = `Delete Selected`
            user.innerHTML = `created by ${details.repo.author}`;
            title.innerHTML = details.repo.title;

            repo.append(title);
            repo.append(user);
            repo.append(selected);

            for (let i = 0; i < details.images.length; i++) {


                let newContent = document.createElement("div");
                newContent.style.borderStyle = "groove"
                newContent.style.margin = "10px"

                let check = document.createElement("input")
                check.setAttribute("type", "checkbox")

                let title = document.createElement("h3");
                title.innerHTML = details.images[i].title

                let newImage = document.createElement("img");
                newImage.setAttribute("src", details.images[i].image);
                newImage.setAttribute("height", "100");


                newContent.append(title);
                newContent.append(check);
                newContent.append(newImage);

                repo.append(newContent);
            }




        })

    //console.log("HEHLDFDF")
    //fetch(`/detail/${repoID}`)


})
