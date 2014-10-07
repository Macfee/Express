# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from logisticsNoManage.models import billStatus, logistics, Country,Area
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import re
import time
import pymssql
import os
from os.path import dirname, basename
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import string


# Create your views here.

def index(request):

    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    return render_to_response("Hello/index.html",{"str":str},context_instance=RequestContext(request))


def translate(request):
    translateCountry = u"翻译国家名称"
    if request.method == "POST":
        countryList = request.POST["country"]
        country = []
        direct = request.POST['language']
        if direct == 'zh2en':
            if countryList:
                s = list(countryList.split('\r\n'))
                for i in range(len(s)):
                    countryDict = {}
                    name = s[i]
                    try:
                        countryValue = Country.objects.get(chineseName = name).englishName
                    except:
                        countryValue = "未翻译成功"
                    countryDict.update({"row":i+1,"orginal":name,"result":countryValue})
                    country.append(countryDict)
                return render_to_response("Hello/translate.html",{"country":country},context_instance=RequestContext(request))
        elif direct=='en2zh':
            if countryList:
                s = list(countryList.split('\r\n'))
                for i in range(len(s)):
                    countryDict = {}
                    name = s[i]
                    try:
                        countryValue = Country.objects.get(englishName = name.upper()).chineseName
                    except:
                        countryValue = "未翻译成功"
                    countryDict.update({"row":i+1,"orginal":name,"result":countryValue})
                    country.append(countryDict)
                return render_to_response("Hello/translate.html",{"country":country},context_instance=RequestContext(request))            
        else:
            return HttpResponse(u"暂时未发现待翻译的国家名，请先核对数据后再进行翻译")
        
    return render_to_response("Hello/translatePage.html",{"translateCountry":translateCountry},context_instance=RequestContext(request))
    
@login_required      
def logisticsNoManage(request):
    title = "单号管理"
    logisticsNo = billStatus.objects.all()
    
    
    if request.method=="POST":
        status = request.POST['status']
        logisticsNo = billStatus.objects.filter(flag=status) 
    paginator = Paginator(logisticsNo, 50)    
    page = request.GET.get('page')
    try:
        listNo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listNo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listNo = paginator.page(paginator.num_pages)
    
    return render_to_response("Logistics/index.html",{"listNo":listNo,"title":title},context_instance=RequestContext(request))

@login_required      
def logisticsNoApply(request):
    title = "申请结果"
    logisticsName = logistics.objects.all()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    if request.method == "POST":
        number = int(request.POST['number']) #申请数量]
        saleman = request.POST['saleman'] #申请人
        channel = request.POST['logisticsName']
        all = billStatus.objects.filter(flag='0').count()
        half = int(all)/2
        if all<int(number):
            return HttpResponse("申请数量已经超出系统数量,请减少数量到%s个" % half)
        else:
            f = None
            selectedNumber = billStatus.objects.filter(flag='0',logisticsName=channel)[:number]
            for value in selectedNumber:
                saveData = billStatus.objects.filter(logisticsNo=value.logisticsNo).update(user=saleman,flag='1',applyTime=now)
                
            data = billStatus.objects.filter(user=saleman,flag = '1',applyTime = now)
            try:
                f=file('%s %s %s.txt' % (time.strftime("%Y-%m-%d", time.localtime()),saleman,number),'w')
                for value in data:
                    f.write(value.logisticsNo)
            except:
                raise
            finally:
                if f:
                    f.close()
            return render_to_response("Logistics/result.html",{"data":data,"title":title},context_instance=RequestContext(request))
    return render_to_response("Logistics/apply.html",{"logisticsName":logisticsName,"title":title},context_instance=RequestContext(request))
    
@login_required    
def logisticsNoUpload(request):
    title = "单号上传"
    logisticsName = logistics.objects.all()
    if request.method == "POST":
        file = request.FILES.get('file',None)
        logisticName = request.POST['logisticsName']
        if file:
            data = file
            fname = file.name
            type = fname[fname.rfind('.'):].replace('.','')
            if type != 'txt':
               return HttpResponse(u"您上传了不符合标准的文件类型,请上传txt格式文件") 
            else:
                lines = file.readlines()
                for line in lines:
                    try:
                        ifNotExist = billStatus.objects.get(logisticsNo = line)
                        pass
                    except:
                        data = billStatus(logisticsNo = line,flag=0,logisticsName = logisticName)
                        data.save()
                return HttpResponse(u'数据保存完成')        
               
    return render_to_response("Logistics/upload.html",{"logisticsName":logisticsName,"title":title},context_instance=RequestContext(request))     
    
def billCalc(request):
    
    if request.method=="POST":
        calcData = request.POST["calcArea"]
        discount = float(request.POST["discount"])/100
        currency = "人民币"
        if calcData:
            s = calcData.split('\r\n')
            priceSheet = []
            for i in range(len(s)):
                data = s[i]
                data = data.split('\t')
                if len(data) > 1 and len(data) != 3:
                    i = i+1
                    return HttpResponse("第%d上传的列数不够" % i)
                    
                for ii in range(len(data)):
                    info = {}
                    if data[ii]:
                        try:
                            pubPrice = Area.objects.get(countryCode = data[1].upper()).price
                            price = round((pubPrice*float(data[2])/1000 + 8.0)*discount,2)
                        except:
                            pubPrice = ''
                            price = u'未知国家无法计算价格'
                        try:
                            country = Country.objects.get(countryCode = data[1].upper()).chineseName
                        except:
                            country = "没有发现该国家简码"
                        info.update({"row":i+1,"logistics":data[0],"country":country,"price":price,"currency":currency,"pubPrice":pubPrice,"weight":float(data[2])/1000,"discount":discount})
                    else:
                        info= {}
                priceSheet.append(info)
            return render_to_response("Hello/calc_result.html",{"priceSheet":priceSheet},context_instance=RequestContext(request))  
    return render_to_response("Hello/calc.html",context_instance=RequestContext(request))
    
def batchNote(request):
    ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        listBillid = request.POST['billid']
        content = request.POST['content']
        editor = request.POST['editor']
        TIME_FORMAT = "%Y-%m-%d %H:%M:%S.000"
        conn=pymssql.connect(host="127.0.0.1",user="sa",password="root",database="0000")
        cursor = conn.cursor()
        listMessage=[]
        if listBillid:
            billidList = listBillid.split('\r\n')
            for billid in billidList:
                
                #获取数据库里最新的数据ID
                sql = "select TOP 1 * from billstatus where billid='%s'" % billid
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    sid = result[0]
                    sql = "insert into billstatusitem (sid,sheetid,sheettype,corpid,billid,note,docman,docdate) VALUES ('%s','0','','lsgj','%s','%s','%s','%s')" % (sid,billid,content,editor,time.strftime(TIME_FORMAT, time.localtime()))
                    cursor.execute(sql.encode("utf8"))
                    conn.commit()
                    message = u'您为 单号为: %s,sid为: %s,备注内容为: %s,编辑人为: %s的快件已经备注完成' % (billid,sid,content,editor)
                else:
                    message = u'单号:%s 在系统里不存在' % billid
                listMessage.append(message)
        cursor.close()
        conn.close()              
        return render_to_response("Hello/note_result.html",{"listMessage":listMessage},context_instance=RequestContext(request))
    return render_to_response("Hello/note.html",{"ip":ip},context_instance=RequestContext(request)) 