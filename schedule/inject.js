// Fix schedule height in Stu-View
// Inject code sinppets below to fix visual issues
// It can be injected using some extension like thise one:
// User JavaScript and CSS
// https://chromewebstore.google.com/detail/user-javascript-and-css/nbhcbdghjpllgmfilhnhkllmkecfmpld

const el = document.querySelector(".fc-time-grid-container");
if (el) {
  const observer = new MutationObserver(() => {
    el.style.height = "1400px";
  });

  observer.observe(el, { attributes: true, attributeFilter: ['style'] });
}



//////////////////////
// D2L colorize CRNs
//////////////////////
console.log('UJSCSS started')

const color_bg_online = "lightgreen";

const courses = [
  {
    name: "PyML",
    semester: "202502",
    color: "lightgreen",
    crns: [
      { crn: "54622", time: "Thu 14:00", color: "lightsalmon" },
      { crn: "58082", time: "Thu 16:30", color: "plum" },
    ],
  },
  {
    name: "TXT",
    semester: "202502",
    color: "lightblue",
    crns: [
      { crn: "57991", time: "Fri 15:00 Zoom", color: color_bg_online },
      { crn: "57993", time: "Fri 15:00 Zoom", color: color_bg_online },
      { crn: "57997", time: "Fri 15:00 Zoom", color: color_bg_online },
    ],
  },
];

for (const course of courses) {
  for (const crn of course.crns) {
    console.log("Injected JS, changing: " + `${course.name} CRN-${crn.crn}-${course.semester}`);
    $(`option:contains(CRN-${crn.crn}-${course.semester})`)
      .css("background-color", crn.color)
      .text(function (_, currentText) {
        return `${course.name} CRN-${crn.crn} - ${crn.time}`;
      });
  }
}
