// This script fetches detailed schedule from StuView in a reasonable CSV format.
// Instructions:
// Go to https://facultyservices.georgebrown.ca/FacultySelfService/ssb/facultyDetailSchedule
// Open dev tools
// Paste the code below into the JS console
// It will print out the schedule in CSV format
// If you have a course with lots of CRNs  use spreadsheet pivot table 
// with SUM(enrollment) as values and Instructor, Code, Days, FromTime as rows

function weekdaysList(weedaysObj) {
    let days = Object.keys(weedaysObj)
    let wdays = []
    for (let day of days) {
        if (weedaysObj[day]) {
            wdays.push(day)
        }
    }
    // return wdays
    // return a string with colon separated weekdays
    let strdays = wdays.join(':')
    // Replace Mon in the beginning with 1_Mon, Tue with 2_Tue and so on
    strdays = strdays.replace(/Mon/, '1_Mon')
    strdays = strdays.replace(/Tue/, '2_Tue')
    strdays = strdays.replace(/Wed/, '3_Wed')
    strdays = strdays.replace(/Thu/, '4_Thu')
    strdays = strdays.replace(/Fri/, '5_Fri')
    strdays = strdays.replace(/Sat/, '6_Sat')
    strdays = strdays.replace(/Sun/, '7_Sun')
    return strdays
}

async function csvSchedule(term='202402') {
    let crnList = `/FacultySelfService/ssb/facultyDetailSchedule/courses?term=${term}`
    let response = await fetch(crnList)
    let data = await response.json()
    let courses = data.courses
    let schedule = []
    for (let course of courses) {
        let crn = course.code

        // fetch course info using the CRN
        // URL example '/FacultySelfService/ssb/facultyDetailSchedule/maintenance?term=202402&crn=57991'
        let cUrl = `/FacultySelfService/ssb/facultyDetailSchedule/maintenance?term=${term}&crn=${crn}` 
        let cResponse = await fetch(cUrl)
        let cData = await cResponse.json()
        let courseInfo = cData.courseInfo
        // loop over courseInfo.meetingList.result
        let meetingList = cData.meetingList.result
        for (let meeting of meetingList) {
            let days = weekdaysList(meeting.daysOfTheWeek)
            let room = meeting.room
            let instructor = meeting.instructors[0].name
            let courseData = [instructor, courseInfo.courseNumber, days, meeting.fromTime, meeting.toTime, room, meeting.scheduleType[0], course.enrollment , crn,  courseInfo.sequenceNumber, courseInfo.courseTitle]
            schedule.push(courseData)
        }
        // break; // For debugging, only get one course
    }

    // Sort schedule by Instructor, then CourseCode, then Days, then FromTime
    // function compval(meeting) {
    //     return String(meeting[7]) + String(meeting[0]) + String(meeting[3]) + String(meeting[4])
    // }
    schedule.sort()

    // print out schedule as CSV
    let csv = 'Instructor,CourseCode,Days,FromTime,ToTime,Room,Type,Enrollment,CRN,Section,Title\n'
    for (let course of schedule) {
        csv += course.join(',') + '\n'
    }
    console.log(csv)

}


// Get the schedule
// Term 202402 is Winter 2025
// The logic is that it's the second term of the academic year that starts in September 2024
csvSchedule('202402')
