/*
 *
 * 토지이용계획 기본 js
 */
//var loadingMsg = "<div style='height:400px'>Loading...</div>";

//택지 관련 사업지구
var homestead_ucode = "UHA100,UHA200,UHA210,UHA220,UHA300,UHA400,UHA500,UHA600,UHA700,UDL100,UDL200,UBK600,UBF100,UBF200,UBF300,UBF400,UBG100,UDW100,UBQ100,UDB100,UBR100,UBV100,UJG100,UDP100,UDE100,UBI100,UBO100,UBO200,UBO300,UBY100,UQQ300,UQQ310,UQQ320";
//homestead_ucode = "UDX200,UNE200"; //test
$(document).ready(function(){
	
	//상세 내용
	$('.action .tab li').click(function(){
		var idx = $(".action .tab li").index(this);
		//console.log("action "+idx);
		
		/*
		0:지역·지구 등 안에서의행위제한내용
		1:행위제한내용 설명+행위가능여부
		*/
		if(idx == 0) {
			document.location.href="#actcon";
			$(".action .tab li:eq(0) a").html("<span class='mb'>지역·지구 등 안에서의 </span>행위제한내용<span class='blind'>선택됨</span>");
			$(".action .tab li:eq(1) a").html("<span class='mb'><span>행위제한내용 설명</span>");
		}
		if(idx == 1) {
			document.location.href="#actcon0";
			$(".action .tab li:eq(0) a").html("<span class='mb'>지역·지구 등 안에서의 </span>행위제한내용");
			$(".action .tab li:eq(1) a").html("<span class='mb'><span>행위제한내용 설명<span class='blind'>선택됨</span></span>");
		}
	});
	
	// 행위제한내용 설명
	$('#act_rusult .tab>ul>li').click(function(){
		var idx = $("#act_rusult .tab li").index(this);
		//console.log("act_rusult "+idx);
		
		/*
		0:행위가능여부
		1:건폐율·용적률
		2:층수·높이제한
		3:건축선
		4:도로조건
		*/
		if(idx > 4) return;
		else document.location.href="#actcon"+idx;
	});
	
	//지역지구등 지정여부
	if($("input[type=hidden][name=mark_ucode]").length > 0) {
		
		var mark_ucodes = "";
		for(var i=0; i < $("input[type=hidden][name=mark_ucode]").length; i++) {
			var id = $($("input[type=hidden][name=mark_ucode]")[i]).val();
			if(i > 0)mark_ucodes += ";";
			mark_ucodes += id;			
		}
		
		$("#markUcodes").val(mark_ucodes);
	}
	
	// 작은글씨확대
	$("#p_adzoom").on("click", function(){
		//console.log("adzoom click");
		if( $("input:checkbox[id='p_adzoom']").is(":checked") )
			$("#adzoom").val("true");
		else
			$("#adzoom").val("");
		$('#frm').submit();
		return false;
	});
	
	// 축척 
	$(".accu .btn_sd:eq(0)").on("click", function(){
		//console.log("btn_sd click");
		//$("#scale").val($("#p_scale").val());
		$("#scale").val($("#scale1").val());
		$("#scaleFlag").val("Y");
		$('#frm').submit();
		return false;
	});


	// 축척 수정
	$("input[name=scale]").on("focus", function(){
		$(this).val('');
	});

	/**
	 * 축척 클릭 이벤트
	 */
	 $("#scale1").on("click", function () {
		 $(".map_scale_select").toggle();
	 });
	 $("#scale1").keydown(function(key) {
         if (key.keyCode == 13) {
        	 $(".accu .btn_sd:eq(0)").trigger( "click" );
         }
     });

	 /**
	  * 축척 사이즈 선택 이벤트
	  */
	 $("#mapSize_select li").on("click", function(){
		 $(this).parent().parent().parent().find("input[name=scale]").val($(this).text());
		 if($(this).text() == "직접입력"){
			 $(this).parent().parent().parent().find("input[name=scale]").val("").focus();
		 }
		 $(".map_scale_select").toggle();
	 });
	 

	
	/**
	 * 인쇄하기 이벤트
	 */
	$(".print_one, .print_all, .print_bt").on("click", function() {
		closeLayer('print_layer');
		
		$("form[name=frm]").find("input[name=p_location]").val(getAddressNm());
		$("form[name=frm]").find("input[name=pnu]").val(getPnu());

		if($(this).attr("name") == 'one'){
			$("form[name=frm]").find("input[name=p_type]").val('one');
		}else if($(this).attr("name") == 'all'){
			$("form[name=frm]").find("input[name=p_type]").val('all');
		}else if($(this).attr("name") == 'chk'){
			$("form[name=frm]").find("input[name=p_type]").val('select');
		}
		$("form[name=frm]").find("input[name=p_type1]").val($("input[type=checkbox][name=p_type1]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type2]").val($("input[type=checkbox][name=p_type2]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type3]").val($("input[type=checkbox][name=p_type3]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type4]").val($("input[type=checkbox][name=p_type4]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type5]").val($("input[type=checkbox][name=p_type5]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type6]").val($("input[type=checkbox][name=p_type6]").prop("checked"));		
		$("form[name=frm]").find("input[name=p_type7]").val($("input[type=checkbox][name=p_type7]").prop("checked"));		
		$("form[name=frm]").find("input[name=scale]").val($("#scale1").val());
		if($("#print_tip").find(".check").length==7){
			$("form[name=frm]").find("input[name=viewType]").val("total");
		}
		
		
		var width = 680;
		var height = 800;
		var x = (screen.availWidth- width)/2;
		var y = (screen.availHeight- height)/2;
		var winState = 'top=' + y + ',left=' + x + ',width=' +width +',height=' +height;
		winState +=',menubar=yes,scrollbars=yes,status=yes,resizable=yes';
		window.open("luLandDetPrintPop.jsp?"+decodeURI($("form[name=frm]").serialize()),"popupPrintOption",winState);
		
	});
	
	//init
	window.onhashchange = fn_changeHash;
	fn_changeHash();
	
	//focus
	if( $("input[type=hidden][name=hash]").val() != "")
	{
		document.location.href="#"+$("input[type=hidden][name=hash]").val();
	}
	
	//resultCode
	if(resultCode == "4008") {
	$("#errorTitle").html("인터넷 서비스가 되지 않는 필지(Code:4008)");
	
		setTimeout(function() {//연락처 가져오는것 0.5초 후 수행. 안그러면 연락처 못가져옴.
			var telBox = $('.schtop_tel'); //지자체 연락처 찾아서 안내 메시지처리
			var title = telBox.contents().filter(function() {
			    return this.nodeType === 3 && $.trim(this.nodeValue) !== '';
			}).text().trim();
		
			var phone = telBox.find('span').first().text().trim();
		
			$("#errorCause").html("해당 시·군·구에서 지역·지구 지정 및 변경, 필지 분할·합병,지적재조사 등 업무를 처리 중인 경우 인터넷 열람이 제한됩니다.<br/>");
			$("#errorMethod").html("긴급하게 토지이용계획 열람이 필요한 경우 <br/>해당 시·군·구<b class='error_sgg_tel'>["+title+" ☎ "+phone+"]</b>로 문의하여 주시기 바랍니다.");
			openLayer("error_layer");
		
		}, 500); 

	}
	else if(resultCode == "4017") {
		setTimeout(function() {//연락처 가져오는것 0.5초 후 수행. 안그러면 연락처 못가져옴.
			var telBox = $('.schtop_tel'); //지자체 연락처 찾아서 안내 메시지처리
	
			var title = telBox.contents().filter(function() {
		 	   return this.nodeType === 3 && $.trim(this.nodeValue) !== '';
			}).text().trim();
	
			var phone = telBox.find('span').first().text().trim();
		
			$("#errorTitle").html("검색이 안되는 필지(Code:4017)");
			$("#errorCause").html("입력한 주소(필지)가 검색되지 않습니다.");
			$("#errorMethod").html("주소를 정확하게 입력하였는지 확인바랍니다.<br/>주소를 정확하게 입력했음에도 검색이 안되는 경우,<br/>해당 시·군·구<b class='error_sgg_tel'>["+title+" ☎ "+phone+"]</b>로 문의하여 주시기 바랍니다.");
			openLayer("error_layer");
		}, 500); 

	}
	else if(resultCode == "9998") {
		$("#errorTitle").html("연결시간이 초과되었습니다.(Code:9998)");
		$("#errorCause").html("접속자수의 증가, 공급되는 정보 데이터양의 초과 등의 이유로 열람 접속 시간이 초과되어 정상적인 서비스가 어려운 경우입니다.");
		$("#errorMethod").html("안내데스크(02-838-4405) 로 조회하시는 필지의 주소를 알려주시면 열람이 가능하도록 조치를 취하겠습니다.");
		openLayer("error_layer");
	}
	else {
		if(errMsg != "")
			alert( errMsg );
	}
	
	//enter print
	$(document).on("keydown", function(e){
		if(e.keyCode == 13){
			if($(".print_layer").css("display") == "block") {
				setTimeout(fn_print_enter, 100);
			}
		}
	});
	
	//실거래가 조회 상태 확인
	$("#kreb_alert").show(); //부동산공시가격 알림이 버튼
	checkKreb();
	
	//상담 지번 보내기
	   $('#btnSendPnu').on('click', async function (e) {
	        e.preventDefault();

	        const pnu = $(this).data('pnu');      // data-pnu="19자리" 로부터 읽음
	        if (!/^\d{19}$/.test(pnu)) {
	            alert('PNU 형식이 올바르지 않습니다.');
	            return;
	        }

	        try {
	            const r = await fetch(
	                `https://help.eum.go.kr:3200/help/sendPnu.jsp?cate=01&pnu=${encodeURIComponent(pnu)}`,
	                { method: 'GET', credentials: 'same-origin' }
	            );

	            if (r.ok) {
	                alert('조회한 지번을 전송하였습니다.');
	            } else if (r.status === 409) {
	                alert('이미 등록된 지번입니다.');
	            } else {
	                throw new Error(`상태코드 ${r.status}`);
	            }
	        } catch (err) {
	            console.error(err);
	            alert('전송에 실패했습니다.');
	        }
	    });
});

function fn_print_enter() {
	$( ".print_bt" ).trigger( "click" );
}



var searchKeyword = "";
var currentPageNo = 1;
function fn_changeHash() {
	//console.log("fn_changeHash = "+window.location.hash);
	
	if(window.location.hash =="" || window.location.hash =="#" || window.location.hash =="#none") {
		//document.location.href="#";
	}
	else if(window.location.hash == "#appoint") {
		//document.location.href="#appoint";
	}
	else if(window.location.hash == "#actcon") {
		//document.location.href="#actcon";
		
		$('#act_menu li').removeClass('on');		
		$('#act_menu li a').removeClass('on');
		tabPannelExt($('.action'), 'tab_content', 0);
		
		$(".action .tab li:eq(0) a").html("<span class='mb'>지역·지구 등 안에서의 </span>행위제한내용<span class='blind'>선택됨</span>");
		$(".action .tab li:eq(1) a").html("<span class='mb'><span>행위제한내용 설명</span>");
	}
	else {
		//document.location.href="#actcon";
		sub = window.location.hash.substring(7,8);
		
		if(sub == "")
			return;
		
		$('#act_menu li').removeClass('on');		
		$('#act_menu li a').removeClass('on');
		tabPannelExt($('.action'), 'tab_content', 1);
		
		$('#act_rusult .tab>ul>li').removeClass('on');
		$('#act_rusult .tab>ul>li a').removeClass('on');
		tabPannelExt($('#act_rusult'), 'tab_content2', sub);
		
		//carGbn = G:건폐율, Y:용적률, C:층수·높이제한, K:건축선, D:도로조건
		if(sub == "0") {
			
			$(".action .tab li:eq(0) a").html("<span class='mb'>지역·지구 등 안에서의 </span>행위제한내용");
			$(".action .tab li:eq(1) a").html("<span class='mb'><span>행위제한내용 설명<span class='blind'>선택됨</span></span>");

			if($.trim($(".anal01").html()) == "") {	
				
				$("#anal01").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetAnal01.jsp",
			    	data:{
			    		"pnu"		: $("#pnu").val(),
			    		"sUcodeListExt"	:sUcodeListExt,
			    		"facilityTableUcodeList"		: facilityTableUcodeList,
			    		"sehUcodeListExt"		: sehUcodeListExt
			    	},
			        type: "post",
			        //contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$("#anal01").html(data);
			        	
			        	//for ready luLandDetAct.js
			        	//시설물 또는 토지이용행위 검색
			        	$('.search_a a:eq(0)').click(function(){
			        		
			        		fn_searchAct($.trim($(".search_a input").val()));
			        		
			        		return false;
			        	});
			        	
			        	//시설물 또는 토지이용행위 검색 취소
			        	$('.search_a a:eq(1)').click(function(){
			        		
			        		$(".search_a input").val('');
			        		fn_searchAct('');
			        		
			        		return false;
			        	});
			        	
			        	$(".search_a input").keydown(function(key) {

			        		if (key.keyCode == 13) {
			        			fn_searchAct($.trim($(this).val()));
			        		}
			        	});
			        	
			        	
			        	//해당 필지에 지정된 「국토의 계획 및 이용에 관한 법률」에 따른 지역 · 지구
			        	$('.act_pop').click(function(){
			        		
			        		$(".act_layer .tbl02").html("");
			        		
			        		var len = $("#resultTb thead tr:eq(1) th").length - 2;
			        		
			        		var contents = "<table summary=\"시설물 또는 토지이용행위 검색 표\">";
			        		contents += "<caption class=\"hidden\">시설물 또는 토지이용행위 검색 표</caption>";
			        		contents += "<colgroup>";
			        		for(var i=0; i < len; i++) {
			        			contents += "<col width=\"\">";
			        		}		
			        		contents += "</colgroup>";
			        		contents += "<thead>";
			        		contents += "<tr><th scope=\"col\" colspan=\""+len+"\" class=\"bg01\">해당 필지에 지정된  「국토의 계획 및 이용에 관한 법률」에 따른 지역 · 지구</th></tr>";																					
			        		contents += "</thead>";
			        		contents += "<tbody>";
			        		contents += "<tr>";
			        		for(var i=0; i < len; i++) {
			        			contents += "<td>"+$("#resultTb thead tr:eq(1) th:eq("+(i+2)+")").text()+"</td>";
			        		}
			        		contents += "</tr>";
			        		
			        		contents += "<tr>";		
			        		for(var i=2; i < len+2; i++) {
			        			contents += "<td>"+$.trim($(this).parent().parent().find("td:eq("+i+")").html())+"</td>";
			        		}
			        		contents += "</tr>";	
			        		contents += "</tbody>";	
			        		contents += "</table>";	
			        		
			        		//console.log(contents);
			        		
			            	$(".act_layer .tbl02").html(contents);
			        	});

			        	//시설물 또는 토지이용행위 셀 merge
			        	$('.tbl02 table tbody tr td a.fold').on('click',function(){
			        		/*
			        		if($(this).hasClass('on')){
			        			$(this).parents('tr').removeClass('on');
			        			$(this).parents('tr').find('a > em').text('+');
			        			$(this).removeClass('on');
			        		} else {
			        			$(this).parents('tr').removeClass('on');
			        			$(this).removeClass('on');
			        			$(this).parents('tr').find('a > em').text('+');
			        			$(this).addClass('on');
			        			$(this).parents('tr').addClass('on');
			        			$(this).parents('tr').find('a > em').text('-');
			        		}
			        		*/
			        		return false;
			        	});
			        	
			        	// 자주 찾는 시설물
			        	$(".flvor_left ul li a").each(function(idx){
			        		$('.flvor_right').find('ul').eq(0).show();
			        		$(this).click(function(){
			        			$(".flvor_left ul li a").removeClass('on');
			        			$(this).addClass('on');
			        			$('.flvor_right').find('ul').hide();
			        			$('.flvor_right').find('ul').eq(idx).show();
			        			return false;
			        		});
			        	});
			        	
			        	//자주 찾는 시설물 상세 - 명칭 길이 처리
			        	$(".flvor_right ul li a").each(function(idx){
			        		if( $(this).text().length > 6)
			        			$(this).addClass("two");
			        	});
			        
			        	if(!fn_isPcSize()) {
			        		$("#resultTb em").parent().attr("colSpan", 3);
			        	}
			        }
			    });
			}

		}
		else if(sub == "1") //건폐율·용적률
		{			
			if($.trim($(".anal02").html()) == "") {	
				
				$(".anal02").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseGYAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "GY"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$(".anal02").html(data);			        	
			        	$("#PopupG_pop").find("span[name=ArService_law]").hide();
			        	$("#PopupY_pop").find("span[name=ArService_law]").hide();
			        	$("#PopupG_popm").find("span[name=ArService_law]").hide();
			        	$("#PopupY_popm").find("span[name=ArService_law]").hide();
			        	
			        	$("#gy_addr").text($("#present_addr").text());
			        	
			        	$(".anal02 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});
			        	
			        	//면적 계산
			        	fn_calArea();
			        	
			        	fn_focusTab("act_rusult",sub);
			        }
			    });
			}
		}
		else if(sub == "2") //층수·높이제한
		{
			if($.trim($(".anal03").html()) == "") {	
				
				$(".anal03").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseCAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		"markUcodes"	: $("input[type=hidden][name=markUcodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "C"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$(".anal03").html(data);
			        	
			        	$("#c_addr").text($("#present_addr").text());
			        	
			        	$(".anal03 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});

			        	//서울특별시 높이관리기준
			        	if($("#pnu").val().substring(0,2) == "11" && $("input[type=hidden][name=mark_ucode]").length > 0) {
			        		
			        		for(var i=0; i < $("input[type=hidden][name=mark_ucode]").length; i++) {
			        			var id = $($("input[type=hidden][name=mark_ucode]")[i]).val();
			        			
			        			if($("#seoul_"+id) && $("#seoul_"+id).html() != undefined) {
			        				$("#seoul_title").show();
			        				$("#seoul_div").show();
			        				$("#seoul_"+id).show();
			        			}
			        		}
			        	}
			        	
			        	//해당하는 지역지구가 없으면	규제사항 항목도 안보여야 함
			        	if( $("#ucodes").val().indexOf("UQA111") == -1
								&& $("#ucodes").val().indexOf("UQA112") == -1
								&& $("#ucodes").val().indexOf("UQA121") == -1
								&& $("#ucodes").val().indexOf("UQA122") == -1
								&& $("#ucodes").val().indexOf("UQA123") == -1
								) {
			        			//$(".anal03 .coverage_wrap").hide();
			        			$(".anal03 .coverage_wrap").html("※ 일조권 높이제한 관련 규제사항이 없습니다. 보다 자세한 사항은 해당 지자체로 문의하시기 바랍니다.");
			        			$(".anal03 .coverage_wrap").parent().find("h4 span").hide();
						}
			        	
			        	fn_focusTab("act_rusult",sub);
			        }
			    });
			}
		}
		else if(sub == "3") //건축선
		{
			
			$("#coverage1").html('<div class="anal_c01_left"><span class="hidden">4미터 미만의 도로와 접한경우½ 만큼 건축선 후퇴</span></div><div class="anal_c01_right"><span class="hidden">4미터 이상의 도로에 모두 접한 경우 도로와 교차각에 따른 필지 모퉁이 부분의 건축선 후퇴</span></div>');
			$("#coverage2").html('<div class="anal_c01_left01"><span class="hidden">4미터 미만의 도로와 접한경우½ 만큼 건축선 후퇴</span></div><div class="anal_c01_right01"><span class="hidden">4미터 이상의 도로에 모두 접한 경우 도로와 교차각에 따른 필지 모퉁이 부분의 건축선 후퇴</span></div>');
			
			if($.trim($("#anal41").html()) == "") {	
				
				$("#anal41").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseKDAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "K"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$("#anal41").html(data);
			        	if($("#anal41").find("#base_dateK").val())
			        		$("#anal4date").html("규제 법령<span>(규제법령 기준일 : "+$("#anal41").find("#base_dateK").val()+")</span>");
			        	else
			        		$("#anal41").html("-");
			        	
			        	$("#anal41 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});
			        }
			    });
			}
			if($.trim($("#anal42").html()) == "") {	
				
				$("#anal42").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseKDAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "K2"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$("#anal42").html(data);
			        	if($("#anal42").find("#base_dateK2").val())
			        		$("#anal4date").html("규제 법령<span>(규제법령 기준일 : "+$("#anal42").find("#base_dateK2").val()+")</span>");
			        	else
			        		$("#anal42").html("-");
			        	
			        	$("#anal42 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});
			        }
			    });
			}
			
			fn_focusTab("act_rusult",sub);
		}
		else if(sub == "4") //도로조건
		{
			if($.trim($("#anal51").html()) == "") {	
				
				$("#anal51").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseKDAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "D"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$("#anal51").html(data);
			        	if($("#anal51").find("#base_dateD").val())
			        	{
				        	$("#anal5date1").html("규제사항<span>(규제법령 기준일 : "+$("#anal51").find("#base_dateD").val()+")</span>");
				        	$("#anal5date2").html("규제 법령<span>(규제법령 기준일 : "+$("#anal51").find("#base_dateD").val()+")</span>");
			        	}
			        	else {
			        		$("#anal51").html("-");
			        	}
			        	
			        	$("#anal51 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});
			        }
			    });
			}
			if($.trim($("#anal52").html()) == "") {	
				
				$("#anal52").html(loadingMsg);
				
				$.ajax({
			    	url: "luLandDetUseKDAjax.jsp",
			    	data:{
			    		"ucodes"	: $("input[type=hidden][name=ucodes]").val(),
			    		//"sggcd"		: $("input[type=hidden][name=sggcd]").val(),
			    		"sggcd"		: $("#pnu").val().substring(0,5),
			    		"pnu"		: $("#pnu").val(),
			    		"carGbn"	: "D2"
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	//console.log(data);
			        	$("#anal52").html(data);
			        	if($("#anal52").find("#base_dateD2").val())
			        	{
				        	$("#anal5date1").html("규제사항<span>(규제법령 기준일 : "+$("#anal52").find("#base_dateD2").val()+")</span>");
				        	$("#anal5date2").html("규제 법령<span>(규제법령 기준일 : "+$("#anal52").find("#base_dateD2").val()+")</span>");
			        	}
			        	else {
			        		$("#anal52").html("-");
			        	}
			        	
			        	$("#anal52 .act_contxt a.link").click(function(){
			        		$(this).parent().next().toggle();
			        		return false;
			        	});
			        }
			    });
			}
			
			fn_focusTab("act_rusult",sub);
		}
		
		
		$(".analysis li a span").remove();
		$(".analysis li:eq("+sub+") a").append("<span class='blind'>선택됨</span>");
	}
	
	
	if(!fn_isPcSize()) {
		setTimeout(fn_reFocus, 500);
	}
}

function fn_reFocus() {
	window.scrollTo(0, eval($(window).scrollTop())-50);
}

//메뉴 포커스
function fn_focusTab(id, sub) {
	//console.log("fn_focus "+id+":"+sub);
	
	if(id == "appoint") {
		//document.location.href="#appoint";
		document.location.href="#";
	}
	else if(id == "act") {
		document.location.href="#actcon";
	}
	else if(id == "act_rusult") {
		document.location.href="#actcon"+sub;
	}
	
	if(!fn_isPcSize() && sub == 0) {
		setTimeout(fn_reFocus, 500);
	}
}

$(window).scroll(function(){
	
	//for mobile app
	if( $("input[type=hidden][name=mobile_yn]").val() == "Y") {
		return;
	}
	
	var sctop = $(window).scrollTop();
	var sw = $(window).width();
	var searchH = $('.search').offset().top;
	var conH = $('.contents').offset().top;
	if(sw > 1262){		
			if(sctop >= conH){
				$(".useplan").stop().css({
						top : sctop - conH + 70
				}, 100);
			} else {
				$(".useplan").stop().css({
						top :0
				}, 100);
			}
			$('.con_left').css('position','').css('z-index','').css('top','');
			//$('.btn_area').css('margin-top','50px')
	}else {
		var conLeft = $('.con_left').offset().top;	
		var btnArea = $('.btn_area').offset().top;	
		if (conLeft <= sctop){	
			$('.con_left').css('position','fixed').css('z-index','99').css('top','0px');
			$('.btn_area').css('margin-top','0')
		} 

		if (sctop < btnArea){
			$('.con_left').css('position','').css('z-index','').css('top','');
			$('.btn_area').css('margin-top','50px')
		}
		
	}
});




$(function(){
	$(".color_in .depth01 > li > a").click(function(){
		$(this).toggleClass('on');
		if($(this).hasClass('on')){
			$(this).next().show();
		} else {
			$(this).removeClass('on');
			$(this).next().hide();
		}
		return false;
	});
});

function allOpen() {
	$('.color_in .depth01 > li > a').addClass('on');
	$('.color_in .depth02').show();

}
function allClose() {
	$('.color_in .depth01 > li > a').removeClass('on');
	if($(this).hasClass('on')){
			
	} else {
		$(this).next().hide();
	}
}


//레이어팝업
var prevLayerName = "";
function openLandLayer(name, val, obj){
	
	if(prevLayerName) closeLayer(prevLayerName);
	openLayer(name);
	prevLayerName = name;

	//인쇄
	if(name =="print_layer") {
		$("input:checkbox[id='p_type1']").prop("checked", true);
		$("input:checkbox[id='p_type2']").prop("checked", true);
		$("input:checkbox[id='p_type3']").prop("checked", true);
		$("input:checkbox[id='p_type4']").prop("checked", true);
	}
	// 연도별보기
	else if(name == "year_layer") {
		
		if($.trim($("#YearJigaList").html()) == "") {
			$("#YearJigaList").html("<tr><td colspan='2'>"+loadingMsg+"</td></tr>");
			
			$.ajax({
		    	url: "luLandDetYearAjax.jsp",
		    	data:{
		    		"pnu"		: $("#pnu").val()
		    	},
		        type: "get",
		        contentType: "application/json; charset=euc-kr",
		        dataType: "html",
		        success : function(data){
		        	$("#YearJigaList").html(data);
		        }
		    });
		}
	}
	// 지정 이력보기
	else if(name == "history_layer") {
		
		$(".history_layer").focus();
		$(".history_layer").html("<div class=\"layer-bg\" style=\"display: block;\"></div><div class=\"layer_content\"><div class=\"layer_content_wrap\">"+loadingMsg+"</div></div></div>");

		$.ajax({
	    	url: "../hs/hsLandDetHistoryPopAjax.jsp",
	    	data:{
	    		"pnu"		: (val != undefined && val != "")?val:$("#pnu").val()
	    	},
	        type: "get",
	        contentType: "application/json; charset=euc-kr",
	        dataType: "html",
	        success : function(data){
				
	        	$(".history_layer").html(data);
				$(".history_layer").show().find(".layer_content").css("top", $(window).scrollTop()+10);
	        	
	        	//현재 정보 복사
	        	if(val) {
	        		$("#his_addr").html( getAddressNm(val) );
	        	}
	        	else {
	        		$("#his_addr").html( $("#present_addr").text() );
	        	}
	        	$("#his_class").html( $("#present_class").html() );
	        	$("#his_area").html( $("#present_area").html() );
	        	$("#his_mark1").html( replaceAll($("#present_mark1").html(),"<a","<aa") );
	        	$("#his_mark2").html( replaceAll($("#present_mark2").html(),"<a","<aa") );
	        	$("#his_mark3").html( replaceAll($("#present_mark3").html(),"<a","<aa") );
	        	
	        	//필지 분할
	        	if($(".his_r_see a") && $(".his_r_see a").length > 0) {
	        		for(i=0; i < $(".his_r_see a").length; i++) {
	        			//$(".his_r_see a:eq("+i+")").attr("href", "javascript:openLandLayer('history_layer', '"+$(".his_r_see a:eq("+i+")").attr("href").split("=")[1]+"');");
	        			$(".his_r_see a:eq("+i+")").attr("onclick", "openLandLayer('history_layer', '"+$(".his_r_see a:eq("+i+")").attr("href").split("=")[1]+"');");
	        			$(".his_r_see a:eq("+i+")").attr("href", "javascript:;");
	        		}
	        	}
	        	
	        	$(".his_area:eq(0)").addClass("mt30");
	        	$(".change_date").hide();
	        	
	        	var tmp = $(".change_d_his03:eq(0)");
	        	tmp.removeClass("change_d_his03");
	        	tmp.addClass("change_d_his00");
	        	//tmp.css("margin-top","37px");
	        	$(".his_area").not(".mt30").find(".change_d_his00").css("margin-top","37px");
	        	
	        	
	        	
	        	if(fn_isPcSize()) {
	        		$(".change_d_his01").hide();
	        		$(".change_date:eq(0)").show();
	        	}

	        	$(".his_present_class").html( $("#present_class_val").val() );
	        	$(".his_present_area").html( $("#present_area").text() );
	        }

	    });
	}
	// 행위가능여부 - 가능여부 보기
	else if(name == "act_layer") {
		if(val != undefined && val != "") {
			
			//건축법 별표외의 포함된 토지이용행위 -> 해당 필지에 지정된 「국토의 계획 및 이용에 관한 법률」에 따른 지역 · 지구 제외
			if(obj) {
				$(".act_layer .tbl02").html("");
			}				
			fn_showActPop(val, obj);
		}
	}
	// 관련정보
	else if(name == "relate_layer") {		
		fn_showRelate(val);
	}
	else {
		//택지 관련 사업지구 확인
		if( name.split("_").length == 4) {
			var ucode = name.split("_")[2];
			//console.log(">>>"+name);
			//console.log(">>>"+ucode);
			//console.log(">>>"+homestead_ucode.indexOf(ucode));
			if(homestead_ucode.indexOf(ucode) > -1) {
				//$("."+name+" .live_bottom").html("");
				
				var p_pnu = $("#pnu").val();
				//if(ucode == "UDX200") p_pnu = "5113010700116300013";
				
				//console.log("p_pnu>>>"+p_pnu);
				
				// 지역/지구 등 안에서의 행위제한 내용 이벤트
		        $.ajax({
			    	url: "luLandDetHomesteadAjax.jsp",
			    	data:{
			    		"pnu"	: p_pnu
			    	},
			        type: "get",
			        contentType: "application/json; charset=euc-kr",
			        dataType: "html",
			        success : function(data){
			        	var prj_code = data.trim();
			        	
			        	//console.log("prj_code>>>"+prj_code);
			        	
			        	if(prj_code == "") {
			        		//정보 없음
							//$("."+name+" .live_bottom").html('<div class="assets"><span><i>!</i>택지정보 지도서비스<em>지정된 사업지구가 없음</em></span></div>');
			        	}
			        	else {
			        		//정보 있음
							$("."+name+" .live_bottom").html('<div class="assets"><span><a href="https://map.jigu.go.kr/mapget.do?zonecode='+prj_code+'" target="_blank"><i>!</i>택지정보 지도서비스</a><em style="padding-right:15px">해당지역 사업지구 정보확인</em></span></div>');
			        	}
			        }
			        //,async: false
			    });  
			}
		}
	}

	return false;
}

// 법령 정보 펼치기
show_detail = function(selectObject, law_cd, joNo, byul_yn, execDt, orderNo, ucode, tblGbn, carGbn) {
	
	test = selectObject;
	
	if($.trim($(selectObject).parent().next().html()) == "") {	
		
		$(selectObject).parent().next().html(loadingMsg);
		
		// 지역/지구 등 안에서의 행위제한 내용 이벤트
        $.ajax({
	    	url: "luLandDetLawContAjax.jsp",
	    	data:{
	    		"law_cd"	: law_cd	,
	    		"jo_no"		: joNo		,
	    		"byul_yn"	: byul_yn	,
	    		"exec_dt"	: execDt	,
	    		"order_no"	: orderNo	,
	    		"ucode"		: ucode,
	    		"tbl_gbn"	: tblGbn,
	    		"car_gbn"	: carGbn
	    	},
	        type: "get",
	        contentType: "application/json; charset=euc-kr",
	        dataType: "html",
	        success : function(data){
	        	$(selectObject).parent().next().html(data);
	        }
	        //,async: false
	    });        
	}
	
	if( $(selectObject).parent().next().css("display") == "none" ) {
		$(selectObject).find("span").html("근거법령 접기펴기 - 현재 확장됨");
		$(selectObject).attr('aria-expanded', true);
	}
	else {
		$(selectObject).find("span").html("근거법령 접기펴기 - 현재 축소됨");
		$(selectObject).attr('aria-expanded', false);
	}
	
}


// 자주 찾는 시설물 조회
function fn_set_luGrStr(name) {
	$(".search_a input").val(name);
	fn_searchAct(name);
	closeLayer('favor_layer');
}


function fn_lwLawDet(area_code, ucode, uname) {
	//console.log(area_code+":"+ucode);
	
	//var openNewWindow = window.open("about:blank");
	//openNewWindow.location.href = context + "/ar/lw/lwLawDet.jsp?ucode="+ucode+"&authCd="+area_code+"&uname="+uname;
	
	if(uname.indexOf("(") > -1) {
		uname = uname.substring(0, uname.indexOf("("));
	}
	
	var popTargetIdx=sessionStorage.getItem("lawPopTargetIdx");
	
	if(popTargetIdx==null){
		popTargetIdx=0;
	}
	targerNm='lawPop'+popTargetIdx;
	
	popTarget=window.open('',targerNm);
	
	try{
		popTarget.name;
	}catch(e){
		popTargetIdx=popTargetIdx*1+1;
		targerNm='lawPop'+popTargetIdx;
		popTarget=window.open('',targerNm);
	}
	
	sessionStorage.setItem("lawPopTargetIdx", popTargetIdx);
	$("#detForm").attr("action",context + "/ar/lw/lwLawDet.jsp?ucode="+ucode+"&authCd="+area_code+"&uname="+uname);
	$("#detForm").attr("target",targerNm);
	$("#detForm").submit();
	
}

function fn_viewBigMap(pnu, scale) {
	
	if(scale == '-1') {
		scale = '';
	}
	
	if( $("#scale1").val() != "") {
		scale = $("#scale1").val();
	}	
	
	window.open(context+'/ar/lu/luLandPop.jsp?pnu='+pnu+'&default_scale='+scale+'&scale='+scale+"&adzoom="+$("#adzoom").val(), '토지이용계획', 'width=640,height=746, top=0,left=0,scrollbars=yes,resizable=1,toolbar=0,menubar=yes,location=0,directories=0,status=1');
	return false;
}


function callKoreps() {
	var koreps_pnu = $("#pnu").val();
	
	if(koreps_pnu == "") return;
	
	var koreps_sect_cd = koreps_pnu.substring(0,5);
	var koreps_loc_cd = koreps_pnu.substring(5,10);
	var koreps_ledg_gbn = koreps_pnu.substring(10,11);
	var koreps_bobn = koreps_pnu.substring(11,15);
	var koreps_bubn = koreps_pnu.substring(15,19);
	
	//test
	var url = "adm_sect_cd="+koreps_sect_cd+"&land_loc_cd="+koreps_loc_cd+"&ledg_gbn="+koreps_ledg_gbn+"&bobn="+koreps_bobn+"&bubn="+koreps_bubn;
	
	//console.log("callKoreps start...");
	
	url = replaceAll(url, "?","^");
	url = replaceAll(url, "&","|");
	//console.log("getUrl : https://api.eum.go.kr/web/api/korep/UrlConnector.jsp" + "?url="+url);	
		
	$.ajax({
		url : "https://api.eum.go.kr/web/api/korep/UrlConnector.jsp" + "?url="+url,
		//url : "/web/tomcat/api_test.xml" + "?url="+url,
		type: "get",
        //contentType: "application/xml; charset=euc-kr",
        dataType: "xml",
        //async: false,
		success : function(res) {
			//console.log(res);
			
			var RESPONSE = $.xml2json(res, true);			
			if(RESPONSE.HEADER[0].CODE[0].text == "0000") {
				var year = RESPONSE.BODY[0].DECSN_JIGA[0].BASE_YEAR[0].text;
				var stdmt = RESPONSE.BODY[0].DECSN_JIGA[0].STDMT[0].text;
				var jiga = comma(RESPONSE.BODY[0].DECSN_JIGA[0].JIGA[0].text);
				var msg = jiga +"원 ("+year+"/"+stdmt+")";
				$("#jiga").text(msg);
			}
			else {
				var msg = "공시지가 정보가 없습니다. (Code : "+RESPONSE.HEADER[0].CODE[0].text+")";
				$("#jiga").text(msg);
			}
			
		},
        error: function(xhr, status, error){
            // 요청이 실패한 경우 실행될 콜백 함수
            console.log("오류 발생: " + error);
        }
	});

	//console.log("callKoreps end...");
}


function checkKreb() {
	$.ajax({
		type:"POST", 
    	url: context + "/ar/lu/luLandDetCheckAjaxXml.jsp",
    	dataType:"json",  
    	data:{
    		"link_sys_id" : "KREB"
    	},
    	async: false,
    	error:function(){   
	        //console.log("예상치 못한 에러가 발생하였습니다.");   
	    }, 
        success : function(data){
        	var mapLuLandDetCheck = $.xml2json(data.mapLuLandDetCheck, true);
        	if(!mapLuLandDetCheck.node[0].text) {
        		var closeRsnDesc = mapLuLandDetCheck.node[0].closeRsnDesc[0].text;
	        	var closeRsnTy = mapLuLandDetCheck.node[0].closeRsnTy[0].text;
	        	//console.log(closeRsnTy+":"+closeRsnDesc);
	        	
	        	$("#jiga").text(closeRsnDesc);
        	}
        	else {
        		callKoreps();
        	}
        },
        complete : function(){
        }
    });
}