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
    $.ajax({url:"/aom/tomcatcommit/",
            data:$('#frm').serialize(),      
            type:"POST",
            dataType:"json",
            success:function(result){         
                if (result.status='false'){
                    alert(result.msg);
                    }
                else{
                    window.location.href = '/aom/installsoftlist';
                }
            },
            error:function (XMLHttpRequest, textStatus, errorThrown){
                 alert('访问网络失败！'+ errorThrown);
                }
            });                                             
}
