#!/usr/bin/env python3
import re

with open('iroom-portal-test.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting fix...")

# 1. Photo CSS
photo_css = '''/* 사진 업로드 */
.photo-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:12px;margin-top:12px}
.photo-item{aspect-ratio:1;border-radius:10px;overflow:hidden;position:relative;background:var(--surface2);border:2px solid var(--border);cursor:pointer;transition:all .2s}
.photo-item:hover{transform:scale(1.02);box-shadow:var(--shadow)}
.photo-item img{width:100%;height:100%;object-fit:cover}
.photo-item .photo-delete{position:absolute;top:4px;right:4px;width:22px;height:22px;background:rgba(220,38,38,0.9);color:#fff;border-radius:50%;font-size:12px;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .15s;cursor:pointer;border:none}
.photo-item:hover .photo-delete{opacity:1}
.photo-comment-badge{position:absolute;bottom:4px;left:4px;width:20px;height:20px;background:rgba(37,99,235,0.9);color:#fff;border-radius:50%;font-size:10px;display:flex;align-items:center;justify-content:center}
.photo-edit-comment{position:absolute;bottom:4px;right:28px;width:20px;height:20px;background:rgba(34,197,94,0.9);color:#fff;border-radius:50%;font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .15s;cursor:pointer;border:none}
.photo-item:hover .photo-edit-comment{opacity:1}
.photo-add{aspect-ratio:1;border-radius:10px;border:2px dashed var(--border);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;background:var(--surface2);flex-direction:column;padding:10px}
.photo-add:hover{border-color:var(--blue);background:var(--blue-l)}
.photo-fullscreen{position:fixed;inset:0;background:rgba(0,0,0,0.95);z-index:500;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .25s}
.photo-fullscreen.open{opacity:1;pointer-events:all}
.photo-fullscreen img{max-width:90vw;max-height:90vh;object-fit:contain;border-radius:8px}
.photo-fullscreen .close-btn{position:absolute;top:20px;right:20px;font-size:32px;color:#fff;cursor:pointer;background:none;border:none}
.photo-fullscreen .download-btn{position:absolute;top:20px;left:20px;padding:10px 20px;background:rgba(37,99,235,0.9);color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600;transition:all .15s}
.photo-fullscreen .download-btn:hover{background:var(--blue);transform:scale(1.05)}'''

content = content.replace('/* 반응형 */', photo_css + '\n/* 반응형 */')
print("1. CSS added")

# 2. 5-stage status
content = content.replace('.status-working{border-color:#fbbf24;background:#fffbeb;color:#92400e}', 
                         '.status-making{border-color:#f97316;background:#fff7ed;color:#c2410c}.status-making::before{background:#f97316}.status-working{border-color:#fbbf24;background:#fffbeb;color:#92400e}')
content = content.replace("working:{label:'접수중',cls:'status-working'},design:{label:'디자인중',cls:'status-design'},ship:{label:'배송중',cls:'status-ship'},done:{label:'완료됨',cls:'status-done'}",
                         "working:{label:'접수중',cls:'status-working'},design:{label:'디자인중',cls:'status-design'},making:{label:'제작중',cls:'status-making'},ship:{label:'배송중',cls:'status-ship'},done:{label:'완료됨',cls:'status-done'}")
content = content.replace("['working','design','ship','done'].forEach", "['working','design','making','ship','done'].forEach")
print("2. Status added")

# 3. Photo modal
photo_modal = '''<div class="photo-fullscreen" id="photoFullscreen" onclick="closePhotoFullscreen(event)">
<button class="close-btn" onclick="closePhotoFullscreen()">X</button>
<button class="download-btn" id="photoDownloadBtn" onclick="downloadCurrentPhoto()">-download</button>
<img id="photoFullscreenImg" src="" alt="">
</div>'''
content = content.replace('<input type="hidden" id="toothInputTarget">', photo_modal + '\n<input type="hidden" id="toothInputTarget">')
print("3. Modal added")

# 4. Photo functions
photo_js = '''function renderPhotoGallery(c){var p=c.photos||[];var m=5;var u=currentUser&&currentUser.type==="admin"&&p.length<m;var h="<div class=photo-gallery>";p.forEach(function(t,i){var d=typeof t==="string"?t:(t.data||"");var cmt=typeof t==="object"?(t.comment||""):"";h+="<div class=photo-item onclick=showPhotoFullscreen("+d+","+c.id+","+i+")><img src="+d+" alt=photo"+(i+1)+">";if(cmt)h+="<div class=photo-comment-badge>B</div>";if(currentUser&&currentUser.type==="admin"){h+="<button class=photo-delete onclick=deletePhoto("+c.id+","+i+")>X</button><button class=photo-edit-comment onclick=editPhotoComment("+c.id+","+i+")>E</button>"}h+="</div>"});if(u){h+="<label class=photo-add><input type=file accept=image/* multiple onchange=handlePhotoUpload("+c.id+",this) style=display:none;><span>+</span></label>"}h+="</div>";return h}function handlePhotoUpload(t,i){var f=i.files;if(!f||f.length===0)return;var c=cases.find(function(x){return x.id===t});if(!c)return;if(!c.photos)c.photos=[];for(var k=0;k<f.length;k++){if(c.photos.length>=5)break;if(f[k].size>5*1024*1024)continue;(function(file){var r=new FileReader();r.onload=function(e){c.photos.push({data:e.target.result,comment:"",uploadedAt:new Date().toISOString()});saveData();var p=document.querySelector(".detail-panel");if(p)p.remove();openDetail(t)}};r.readAsDataURL(file)})(f[k])}}function deletePhoto(t,i){if(!confirm("delete?"))return;var c=cases.find(function(x){return x.id===t});if(!c||!c.photos)return;c.photos.splice(i,1);saveData();var p=document.querySelector(".detail-panel");if(p)p.remove();openDetail(t)}function editPhotoComment(t,i){var c=cases.find(function(x){return x.id===t});if(!c||!c.photos||!c.photos[i])return;var p=c.photos[i];var cur=typeof p==="object"?(p.comment||""):"";var n=prompt("comment:",cur);if(n!==null){c.photos[i].comment=n;saveData();var p=document.querySelector(".detail-panel");if(p)p.remove();openDetail(t)}}var curUrl="",curName="";function showPhotoFullscreen(u,t,i){var m=document.getElementById("photoFullscreen"),img=document.getElementById("photoFullscreenImg");if(!m||!img)return;curUrl=u;curName="case"+(t||"p")+(i!==undefined?i:"")+".jpg";img.src=u;m.classList.add("open");document.body.style.overflow="hidden"}}function downloadCurrentPhoto(){if(!curUrl)return;var l=document.createElement("a");l.href=curUrl;l.download=curName;l.click()}function closePhotoFullscreen(e){if(e&&e.target!==e.currentTarget)return;var m=document.getElementById("photoFullscreen");if(m){m.classList.remove("open");document.body.style.overflow=""}}}'''

content = content.replace("function deleteCase(id) {\n  if(!confirm('삭제하시겠습니까?')) return;",
                         photo_js + "\n\nfunction deleteCase(id) {\n  if(!confirm('삭제하시겠습니까?')) return;")
print("4. Functions added")

# 5. Photo section in detail
content = content.replace("` : ''}\n    </div>\n  `;\n  \n  if(currentUser.type === 'admin') {",
                         "` : ''}\n    </div>\n    <div class=\"panel-section\"><div class=\"panel-section-title\">photo</div><div style=\"margin-top:12px;\">${renderPhotoGallery(c)}</div></div>\n  `;\n  if(currentUser.type === 'admin') {")
print("5. Section added")

# 6. Photo badge in table
content = content.replace("const typeLabel = isRemake ? '<span style=\"color:var(--red);font-weight:700;\">🔄 리메이크</span>' : (c.unitType === 'bridge' ? '브릿지' : '싱글');\n    const dateDisplay",
                         "const typeLabel = isRemake ? '<span style=\"color:var(--red);font-weight:700;\">🔄 리메이크</span>' : (c.unitType === 'bridge' ? '브릿지' : '싱글');\n    var photoCount = (c.photos || []).length;\n    const dateDisplay")
content = content.replace("<td><strong>${getDisplayPatient(c)}</strong></td>",
                         "<td><strong>${getDisplayPatient(c)}</strong>${photoCount>0?'<span style=color:var(--blue);>P'+photoCount+'</span>':''}</td>")
print("6. Badge added")

# 7. Photos in localStorage
content = content.replace("if(c.isRemake === undefined) c.isRemake = false;\n    });",
                         "if(c.isRemake === undefined) c.isRemake = false;\n      if(!c.photos) c.photos = [];\n    });")
content = content.replace("created_at: c.createdAt || null\n      }, { onConflict: 'id' })",
                         "created_at: c.createdAt || null,\n        photos: c.photos || []\n      }, { onConflict: 'id' })")
print("7. Storage added")

with open('iroom-portal-test.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== DONE ===")
