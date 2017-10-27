//表单校验
function checkform(){
    //alert($('#frm').serialize())
    var select=document.getElementById("nodeselect")
    if (select.length==0){
        alert('未选中任何节点')
        return false;
    }
    for (var i=0;i<select.length;i++)
    {
      select[i].selected=true; 
      }
    return true;
}    

//提交表单
function commit(){
    if (checkform()!=true){return false;}
    var data={url:"/aom/tomcatcommit/",
              data:$('#frm').serialize(),
              success:callback,
              error:callbackerror,}
    putdata(data);              
}

function callback(result){
    if (result.status='false'){
        alert(result.msg);
        }
    else{
        window.location.href = '/aom/installsoftlist';
    }
}