
document.addEventListener('DOMContentLoaded', function () {

    const repo = document.querySelector('#repo-detail')
    const repoID = document.URL.split("/")[document.URL.split("/").length - 1]
    
    fetch(`/repo_details/${repoID}`)
        .then(response => response.json())
        .then(details => {
            console.log(details);
            let title = document.createElement("h2");
            let user = document.createElement("h5");

            

            let addImage = document.createElement("button");
            addImage.innerHTML = "Add Image"
            addImage.addEventListener("click", function () {
                console.log("add image")
                window.location.href = `/upload/${repoID}`
            })

            let selectAll = document.createElement("button");
            selectAll.innerHTML = "Select All"
            selectAll.addEventListener("click", function () {
                checks = document.querySelectorAll('input[name="image"]');
                for (let i = 0; i < checks.length; i++) {
                    checks[i].checked = true
                }
            })

            let unSelectAll = document.createElement("button");
            unSelectAll.innerHTML = "Unselect All"
            unSelectAll.addEventListener("click", function () {
                checks = document.querySelectorAll('input[name="image"]');
                for (let i = 0; i < checks.length; i++) {
                    checks[i].checked = false
                }
            })

            let selectOption = document.createElement("select");

            let option0 = document.createElement("option");
            option0.setAttribute("value", "delete");
            option0.innerText = "Delete Selected";

            let option1 = document.createElement("option");
            option1.setAttribute("value", "download");
            option1.innerText = "Download Selected";

            selectOption.append(option1);
            selectOption.append(option0);

            let selected = document.createElement("button");


            selected.innerHTML = `Submit`
            user.innerHTML = `created by ${details.repo.author} on ${details.repo.timestamp}`;
            title.innerHTML = details.repo.title;

            repo.append(title);
            repo.append(user);
            repo.append(selectOption);
            repo.append(selected);
            repo.append(selectAll);
            repo.append(unSelectAll);
            
            if(details.user == details.repo.author) {
                let deleteButton = document.createElement("button")
                deleteButton.innerText = "Delete Repo"
                deleteButton.addEventListener("click", function(){
                    window.location.href = `/delete-repo/${repoID}`
                })
                repo.append(addImage);
                repo.append(deleteButton)
            }
            

            selected.addEventListener('click', function () {

                checks = document.querySelectorAll('input[name="image"]:checked');
                theOption = document.querySelector("select")

                if (theOption.value == "delete") {
                    for (let i = 0; i < checks.length; i++) {
                        fetch(`/delete-image/${details.images[checks[i].id].id}`)
                            .then(response => response.json())
                            .then(ans => {
                                if (i == checks.length - 1) {
                                    location.reload();
                                }
                            })
                    }
                }
                else if (theOption.value == "download") {
                    for (let i = 0; i < checks.length; i++) {


                        let element = document.createElement("a");
                        element.setAttribute('href', details.images[checks[i].id].image);
                        element.setAttribute("download", "download")

                        element.click()
                    }

                }

            })
            imageArray = Object.values(details.images)

            for (let i = 0; i < imageArray.length; i++) {


                let newContent = document.createElement("div");
                newContent.style.borderStyle = "groove";
                newContent.style.margin = "10px";

                let label = document.createElement("label");
                label.setAttribute("for", imageArray[i].title);

                let check = document.createElement("input");
                check.setAttribute("type", "checkbox");
                check.setAttribute("id", imageArray[i].title);
                check.setAttribute("name", "image");

                label.append(check);




                let title = document.createElement("h3");
                title.innerHTML = imageArray[i].title;

                let newImage = document.createElement("img");
                newImage.setAttribute("src", imageArray[i].image);
                newImage.setAttribute("height", "100");

                let editButton = document.createElement("button");
                editButton.innerHTML = "Edit"
                editButton.addEventListener("click",function() {
                    console.log("Hello")
                    window.location.href = `/edit-image/${imageArray[i].id}`
                })

                newContent.append(title);
                newContent.append(label)
                newContent.append(newImage);
                if(details.user == details.repo.author) {
                    newContent.append(editButton);
                }
                

                repo.append(newContent);
            }

        })
})
