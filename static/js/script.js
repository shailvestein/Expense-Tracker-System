function confirmSave(){
  let confirmAction = confirm("Are you sure wanted to save your hisab?");
  if (confirmAction){
    document.getElementById('save_hisab_btn').submit();
  } else{
    alert("Hisab didn't saved!");
  }
}

function confirmPaymentDone(){
  let confirmPayment = confirm("Have you got your extra spent money?")
  if (confirmPayment){
    document.getElementById("markPaymentDone").submit();
  }else{
    alert("Payment didn't marked as done!");
  }
}