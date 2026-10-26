import { chromium } from 'playwright';
import fs from 'fs';
const b = await chromium.launch({executablePath:'/usr/bin/chromium'});
const pg = await b.newPage({ viewport:{width:430,height:1200}, deviceScaleFactor:2 });
const db = JSON.parse(fs.readFileSync('/workspace/保险产品43款-V1022P版-已核对完整.json','utf8'));
await pg.goto('http://localhost:8077/index.html',{waitUntil:'networkidle'});
await pg.evaluate((d)=>localStorage.setItem('ins_v1', JSON.stringify({app:'insurance-compare',products:d.products,weights:d.weights||{},family:{members:[]},health:{},settings:{}})), db);
await pg.reload({waitUntil:'networkidle'});
await pg.waitForTimeout(500);
await pg.evaluate(()=>{
  const list=['imp-yw-dhj9','imp-yw-dhj8'].map(i=>appData.products.find(p=>p.id===i));
  const html=renderReportView(list);
  const box=document.getElementById('page-report')||document.getElementById('pages');
  box.innerHTML=html;
});
await pg.waitForTimeout(300);
const el = await pg.$('.rpt-scroll');
await el.screenshot({path:'/tmp/style.png'});
await b.close();
