
(function(){
  "use strict";
  const list=document.getElementById("daily-list");
  if(!list)return;
  const cards=Array.from(list.querySelectorAll("[data-date]"));
  const date=document.getElementById("date-filter");
  const year=document.getElementById("year-filter");
  const month=document.getElementById("month-filter");
  const reset=document.getElementById("reset-filter");
  const status=document.getElementById("filter-status");
  const empty=document.getElementById("filter-empty");
  const params=new URLSearchParams(location.search);
  if(date && /^\d{4}-\d{2}-\d{2}$/.test(params.get("date")||""))date.value=params.get("date");
  function apply(){
    const wanted=(date&&date.value)||"";
    const wantedYear=(year&&year.value)||"";
    const wantedMonth=(month&&month.value)||"";
    let n=0;
    for(const card of cards){
      const day=card.dataset.date||"";
      const visible=(!wanted||day===wanted)&&(!wantedYear||day.startsWith(wantedYear+"-"))&&(!wantedMonth||day.slice(5,7)===wantedMonth);
      card.hidden=!visible;
      if(visible)n++;
    }
    if(status)status.textContent="显示 "+n+" / "+cards.length+" 个日期";
    if(empty)empty.hidden=n!==0;
  }
  for(const x of [date,year,month])if(x)x.addEventListener("change",apply);
  if(reset)reset.addEventListener("click",function(){
    if(date)date.value="";
    if(year)year.value="";
    if(month)month.value="";
    apply();date?.focus();
    if(location.protocol!=="file:")history.replaceState(null,"",location.pathname+location.hash);
  });
  apply();
})();
