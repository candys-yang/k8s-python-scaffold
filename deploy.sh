#!/bin/bash


echo '

 ┌───────────────────────────────────────────────────┐ 
   Deploy Config                              
'

# 到 README.md 取版本号
export ver=`cat README.md | grep '>version:' | awk '{print $2}'`

# Docker打包配置
export buildurl='meidongauto-docker.pkg.coding.net/itsm/private/'
export imagename='images-name'

# Kubernetes 配置
export token=''
export k8sser='https://42.157.195.68:6443'
export deployment='deployment_name'
export container='container_name'


echo '    version: '$ver
echo '    imageurl: '$buildurl
echo '    imagename: '$imagename
echo '    deployment: '$deployment
echo '    containers: '$container
echo '
 └───────────────────────────────────────────────────┘

'

# docker打包
docker build ./ -t $buildurl$imagename':'$ver
docker push $buildurl$imagename':'$ver

# 部署到k8s
echo '

 ┌───────────────────────────────────────────────────┐ 

   Deploy To K8s                                     

 └───────────────────────────────────────────────────┘

'

	curl -k -X PATCH\
	 -H "Authorization: Bearer $token"\
	 -H "Content-Type: application/strategic-merge-patch+json"\
	 --data '
   {"spec":{
     "template":{
       "spec":{
         "containers":[
           {"name":"'$container'","image":"'$buildurl$imagename':'$ver'"}
          ]}}}}'\
 $k8sser/apis/apps/v1/namespaces/itsm/deployments/$deployment


echo '


 ┌───────────────────────────────────────────────────┐  

   Deploy Complete.                                   

 └───────────────────────────────────────────────────┘


'
