
document.addEventListener('DOMContentLoaded', function () {

    const repo = document.querySelector('#repo-detail')
    const imgList = document.querySelector('#img-list')
    const repoID = document.URL.split("/")[document.URL.split("/").length - 1]
    
    fetch(`/repo_details/${repoID}`)
        .then(response => response.json())
        .then(details => {
            console.log(details);
            let title = document.createElement("h2");
            let user = document.createElement("h5");

            

            let addImage = document.createElement("button");
            
            addImage.innerHTML = "Add Image"
            addImage.setAttribute("class","btn btn-primary")
            addImage.addEventListener("click", function () {
                console.log("add image")
                window.location.href = `/upload/${repoID}`
            })

            let selectAll = document.createElement("button");
            selectAll.innerHTML = "Select All"
            selectAll.setAttribute("class","btn btn-outline-secondary")
            selectAll.addEventListener("click", function () {
                checks = document.querySelectorAll('input[name="image"]');
                for (let i = 0; i < checks.length; i++) {
                    checks[i].checked = true
                }
            })

            let unSelectAll = document.createElement("button");
            unSelectAll.innerHTML = "Unselect All"
            unSelectAll.setAttribute("class","btn btn-outline-secondary")
            unSelectAll.addEventListener("click", function () {
                checks = document.querySelectorAll('input[name="image"]');
                for (let i = 0; i < checks.length; i++) {
                    checks[i].checked = false
                }
            })

            let selectOption = document.createElement("select");
            selectOption.setAttribute("class","form-select")

            let option0 = document.createElement("option");
            option0.setAttribute("value", "delete");
            option0.innerText = "Delete Selected";

            let option1 = document.createElement("option");
            option1.setAttribute("value", "download");
            option1.innerText = "Download Selected";

            selectOption.append(option1);
            if(details.user == details.repo.author) {
                selectOption.append(option0);
            }
            

            let selected = document.createElement("button");
            selected.innerHTML = `Submit`
            selected.setAttribute("class","btn btn-success")
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
                deleteButton.setAttribute("class","btn btn-danger")
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
                let card = document.createElement("div");
                card.setAttribute("class","card");
                card.setAttribute("style","width: 250px;")
                //card.setAttribute("style","height: 500px;")

                let newContent = document.createElement("div");
                newContent.setAttribute("class","card-body")

                let label = document.createElement("label");
                label.setAttribute("for", imageArray[i].title);
                label.innerHTML = "Select"
                label.setAttribute("class","btn btn-outline-primary")

                let check = document.createElement("input");
                check.setAttribute("type", "checkbox");
                check.setAttribute("class","btn-check")
                check.setAttribute("id", imageArray[i].title);
                check.setAttribute("name", "image");
                check.setAttribute("autocomplete","off")
                

                //label.append(check);
                




                let title = document.createElement("h3");
                title.innerHTML = imageArray[i].title;
                title.setAttribute("class","card-title")

                let newImage = document.createElement("img");
                newImage.setAttribute("src", imageArray[i].image);
                newImage.setAttribute("height", "100");
                newImage.setAttribute("class","img-fluid rounded-start")

                let editButton = document.createElement("button");
                editButton.setAttribute("class","btn btn-outline-secondary")
                editButton.innerHTML = "Edit"
                editButton.addEventListener("click",function() {
                    console.log("Hello")
                    window.location.href = `/edit-image/${imageArray[i].id}`
                })

                card.append(newImage)
                card.append(newContent)
                newContent.append(title)
                newContent.append(check)
                newContent.append(label)
                
                
                
                if(details.user == details.repo.author) {
                    newContent.append(editButton);
                }
                
                imgList.append(card);
                //repo.append(card);
            }

        })
})
