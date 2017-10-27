//初始化客户
var customjson={'data':{'page':'syncnginxconf',
                        'type':'getcustom'},
                'url':"/aom/postData/",
                'success':callbackcustom,
                'error':callbackerror,}
       
$(document).ready(putdata(customjson));

//生成project
function putProject(){
    if ($('#custom').val()!=null){
        var data={'page':'syncnginxconf','type':'getproject','custom':$('#custom').val()};
        var projectjson={'data':data,
                        'url':"/aom/postData/",
                        'success':callbackproject,
                        'error':callbackerror,}
        putdata(projectjson);
    }
    else{
        clearselect($('#project'));
    }
}

//生成environment
function putEnvironment(){     
    if ($('#project').val()!=null){              
        var data={'page':'syncnginxconf','type':'getenvironment','project':$('#project').val()};
        var projectjson={'data':data,
                        'url':"/aom/postData/",
                        'success':callbackenvironment,
                        'error':callbackerror,}
        putdata(projectjson);
    }
    else{
        clearselect($('#environment'));
    }
}

//生成环境信息,
function callbackenvironment(result){
    initselect($('#environment'),result.table);   
}

//生成项目信息,
function callbackproject(result){
    initselect($('#project'),result.table);   
    putEnvironment();
}

//生成客户信息,
function callbackcustom(result){
    initselect($('#custom'),result.table);
    putProject();
    
}        

//表单验证
function checkform(){
    if ($('#custom').val()!=null && $('#project').val()!=null && $('#environment').val()!=null){
        //alert($('#environment').val)
        return true;
    }
    else{
        alert('客户、项目、环境都不可为空。');
        return false;
    }
}

//提交表单
function commit(){
    if (checkform()!=true){return false;}
    var data={url:"/aom/syncnginxconfcommit/",
              data:$('#frm').serialize(),
              success:callback,
              error:callbackerror,}
    putdata(data);              
}

function callback(){
    window.location.href = '/aom/syncnginxconflist'
}
