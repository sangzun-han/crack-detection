const mobileSearchField = document.querySelector("#mobileSearchField");
const cardOutput = document.querySelector(".card-output");
const cardWrap = document.querySelector(".cardWrap");

cardOutput.style.display = "none";

mobileSearchField.addEventListener("keyup", (event) => {
  const searchValue = event.target.value;

  if (searchValue.trim().length > 0) {
    cardOutput.innerHTML = "";
    fetch("/mobileSearch", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        cardWrap.style.display = "none";
        cardOutput.style.display = "block";

        if (data.length === 0) {
          result.style.display = "block";
          cardOutput.style.display = "none";
        } else {
          result.style.display = "none";
          data.map((item) => {
            if (item.isFlattened == true) {
              item.isFlattened = "O";
            } else {
              item.isFlattened = "X";
            }

            cardOutput.innerHTML += `
            <div class="d-flex justify-content-center" id="card">
            <div class="card mb-3" style="max-width: 80%;">
              <div class="row g-0">
                <div class="col-md-4">
                <a href="/db/${item.id}"><img src="/media/${item.image}" class="img-fluid rounded-start" alt="image" /></a>
                </div>
                <div class="col-md-8">
                  <div class="card-body">
                    <h5 class="card-title">카테고리 : ${item.category_name}</h5>
                    <p class="card-text">현황 : ${item.state}</p>
                    <p class="card-text">원인 : ${item.cause}</p>
                    <p class="card-text">조치방안 : ${item.solution}</p>
                    <p class="card-text"><small class="text-muted">평탄화작업 : ${item.isFlattened}</small></p>  
                  </div>
                </div>
              </div>
            </div>
          </div>
            `;
          });
        }
      });
  } else {
    cardOutput.style.display = "none";
    result.style.display = "none";
    cardWrap.style.display = "block";
  }
});
