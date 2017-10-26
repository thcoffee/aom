//初始化客户
var customjson={'data':{'page':'syncnginxconf',
                        'type':'getcustom'},
                'url':"/aom/postData/",
                'success':callbackcustom,
                'error':callbackerror,}
       
$(document).ready(putdata(customjson));

//生成project
function putProject(){
    var data={'page':'syncnginxconf','type':'getproject','custom':$('#custom').val()};
    var projectjson={'data':data,
                    'url':"/aom/postData/",
                    'success':callbackproject,
                    'error':callbackerror,}
    putdata(projectjson);
}

//生成environment
function putEnvironment(){                   
    var data={'page':'syncnginxconf','type':'getenvironment','project':$('#project').val()};
    var projectjson={'data':data,
                    'url':"/aom/postData/",
                    'success':callbackenvironment,
                    'error':callbackerror,}
    putdata(projectjson);
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


//表单提交
function commit(){
    $.ajax({url:"/aom/jdk/",
            data:$('#frm').serialize(), 
            type:"POST",
            dataType:"json",
            success:function(result){         
                window.location.href = '/aom/installsoftlist'
            },
            error:function (XMLHttpRequest, textStatus, errorThrown){
                 alert('访问网络失败！'+ errorThrown);
                }
            }
    );                       
}
