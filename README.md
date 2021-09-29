
## Image Contour

<div>
  <img src="https://user-images.githubusercontent.com/57563053/135246483-1aa32147-7a5f-46a6-932c-7eda6cb92f96.png" width="400" height="300"/>
  <img src="https://user-images.githubusercontent.com/57563053/135246486-3910899d-df84-46f4-a5fd-baa120ffb971.png" width="400" height="300"/>
</div>
<p>마커가 있으면 마커도 threshold에 걸려서 같이 인식됨 곡선만 따로 컨투어를 얻어낼 방법을 모르겠음 -> 찾아보는중 </p>

<div>
  <img src="https://user-images.githubusercontent.com/57563053/135246466-8b1523d6-042b-460f-a859-d8f9d69bc6ec.png" width="400" height="300"/>
  <img src="https://user-images.githubusercontent.com/57563053/135246472-41da3f3c-3a97-4514-9620-d5789f9aa537.png" width="400" height="300"/>
</div>
<p>마커가 없으면 약간의 노이즈는 존재하지만 Image Contour가 가능 -> 길이를 잴 방법이 없음 cv2.arclength()를 이용해 길이를 재는방법이 있는데 단위를 알수 없기도하고 값이 이상하게 나옴</p>
