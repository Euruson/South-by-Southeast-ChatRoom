function checknm(){
	if(frmLogin.txtName.value==""){
		var txtName=document.getElementById("txtName");
        txtName.style.borderColor="red";
        var accWarning=document.getElementById("accWarning");
        accWarning.removeAttribute("hidden");
		return false;
	}
	else
		return true;		
}
function focusnm(){
	var txtName=document.getElementById("txtName");
    txtName.style.borderColor="#DFDFDF";
    var accWarning=document.getElementById("accWarning");
    accWarning.setAttribute("hidden",true);
}


function checkpw(){
	if (frmLogin.txtPwd.value.length < 6) {
        //alert("密码不能小于6位");
        //frmLogin.txtPwd.focus();
        var txtPwd=document.getElementById("txtPwd");
        txtPwd.style.borderColor="red";
        var pwdWarning=document.getElementById("pwdWarning");
        pwdWarning.removeAttribute("hidden");
        //frmLogin.txtPwd.value = null;
		return false;
    }
	else
		return true;			
}
function focuspw() {
	var txtPwd=document.getElementById("txtPwd");
    txtPwd.style.borderColor="#DFDFDF";
    var pwdWarning=document.getElementById("pwdWarning");
    pwdWarning.setAttribute("hidden",true);
}

function recheckpw(){
	
	if(frmLogin.ctxtPwd.value!=frmLogin.txtPwd.value||frmLogin.ctxtPwd.value==""){
		var ctxtPwd=document.getElementById("ctxtPwd");
        ctxtPwd.style.borderColor="red";
        var cpwdWarning=document.getElementById("cpwdWarning");
        cpwdWarning.removeAttribute("hidden");
		return false;
	}			
	else{
        var ctxtPwd=document.getElementById("ctxtPwd");
        ctxtPwd.style.borderColor="#DFDFDF";
        var cpwdWarning=document.getElementById("cpwdWarning");
        cpwdWarning.setAttribute("hidden",true);
		return true;
    }
}
function focusrpw(){
	var ctxtPwd=document.getElementById("ctxtPwd");
    ctxtPwd.style.borderColor="#DFDFDF";
    var cpwdWarning=document.getElementById("cpwdWarning");
    cpwdWarning.setAttribute("hidden",true);
}


function checkrnm(){
	if(frmLogin.txtRname.value==""){
		//alert("真实姓名不能为空!");
		//frmLogin.txtRname.focus();
		return false;
	}		
}
function checkhm(){
	if(frmLogin.txtHome.value==""){
		//alert("家庭住址不能为空!");
		//frmLogin.txtHome.focus();
		return false;
	}		
}

function submitForm(){
	if(checknm()==true&&checkpw()==true&&recheckpw()==true){
		if(checkemail()==true){
			if(confirm('请查收注册确认邮件！')){
				// this.form.action="UserReview.asp?action=delall" //设置处理程序
				this.form.submit(); //提交表单
			}
            else
            {
                alert("!!!");
            }
		}
        else
            {
                alert("目前本聊天网站只对南京大学生开放！");
            }
	}
	else{
		alert("请完善信息");
	}
}
function checkemail(){
	var email=document.getElementById("email");
	if(email.value.indexOf("@seu.edu.cn")<0&&email.value.indexOf("@nju.edu.cn")<0&&email.value.indexOf("@njust.edu.cn")<0&&email.value.indexOf("@njupt.edu.cn")<0
    &&email.value.indexOf("@njue.edu.cn")<0&&email.value.indexOf("497425817@qq.com")<0)
	{
		alert("邮箱不合法");
		return false;
	}
	else
		return true;
}
function changeBg(){
	var bg_img=["../static/images/bg_01.jpg",
        "../static/images/bg_02.jpg",
        "../static/images/bg_03.jpg",
        "../static/images/bg_04.jpg",
		"../static/images/bg_06.jpg"]//这里可以添加图片路径，每个路径用""包起来，每个路径之间用逗号分开，要在英文状态下输入符号。
       
    document.getElementById("regbody").style.background="url("+bg_img[Math.floor(Math.random()*(bg_img.length))]+")";
	document.getElementById("regbody").style.backgroundSize="cover";  //设置随机背景图，这里不用改。
	document.getElementById("regbody").style.backgroundAttachment="fixed";
	document.getElementById("regbody").style.fontFamily='"Microsoft YaHei",微软雅黑,"MicrosoftJhengHei",华文细黑,STHeiti,MingLiu';
}
