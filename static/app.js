
async function getAllCupcakes() {
  response = await axios.get("/api/cupcakes")
  let cupcakes = response.data.cupcakes

  // clear cupcake list
  $("#cupcake-list").empty()

  for (let cupcake of cupcakes) {
    $("#cupcake-list").append(`<li>${cupcake.flavor}</li>`)
  }
}

async function submitForm(e){
  e.preventDefault();

  let sendData = {}
  for (let i=0; i<e.target.length-1; i++) {
    let field = e.target[i]
    
    sendData[field.name] = field.value
  }

  response = await axios.post("/api/cupcakes", sendData)

  getAllCupcakes();
}


$(document).ready(async function(){
  getAllCupcakes();
  $("#create-form").on('submit', submitForm);
})