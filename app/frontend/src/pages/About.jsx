import React from 'react'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"


const About = () => {
  return (
    <div>
      <div className='font-inter font-semibold text-3xl text-center mt-10'>
        Why I made ClassConnect?
      </div>
      <div className='font-inter font-medium text-lg mt-10 ml-20 mr-20'>
        Back in my first year, my daily routine included a not-so-fun ritual: manually scheduling all my classes in Google Calendar. I’d flip between pages in academia or stare at a timetable image, then painstakingly add them to my calendar. Every. Single. Day.
          <br />
          <br />
        It was boring. It was repetitive. And, honestly, it was frustrating. I knew there had to be a smarter way. Around this time, I started hearing my classmates and friends wishing for the same thing—a simpler, more efficient way to manage their schedules. I even stumbled across a public group where someone explained how they lived by their calendar and needed a tool to make scheduling classes easier.

        <br />
        <br />

        That’s when it clicked: If people, including me, needed this, why not create it? So I did. Welcome to ClassConnect. With this app I’ve turned that manual and time-consuming process into something seamless and automatic. And with notifications, you’ll always stay one step ahead.

        <br />
        <br />
        Who needs to sit and manually add classes when you can just download a ready-made .ical file? ClassConnect turns your timetable into an instant calendar upload, saving you time and effort so you can focus on what really matters.
      </div>

      <div className='mb-20'>
        <div className='font-inter font-semibold text-3xl text-center mt-20 '>
          FAQs
        </div>
          <div className='mx-40 mt-10 '>
          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>How do I add it to Calendar?</AccordionTrigger>
              <AccordionContent>
              On successful login, you will be redirected to the download page. Once your timetable is scraped and converted into an iCal file, you can download it and click on the file downloaded and select add all option to add all your classes to your calendar.
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>What platforms does ClassConnect support?</AccordionTrigger>
              <AccordionContent>
              This .ics file format is widely supported across many calendar applications like Google Calendar, Apple Calendar and more. 
              </AccordionContent>
          </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>Can I trust ClassConnect with my data?</AccordionTrigger>
              <AccordionContent>
              Absolutely! Your data is used only for logging in to Academia for scraping your classes and is never stored anywhere. 
              </AccordionContent>
          </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>What to do if I have an issue with ClassConnect?</AccordionTrigger>
              <AccordionContent>
              Please do contact me through mail : meyyappan055@gmail.com or through whatsapp : +91 8903042799
              </AccordionContent>
          </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>How does ClassConnect handle holidays or breaks?</AccordionTrigger>
              <AccordionContent>
                ClassConnect will automatically account for holidays or breaks if they are included in Academia's Calendar, ensuring your calendar stays accurate.
              </AccordionContent>
          </AccordionItem>
          </Accordion>

          </div>
      </div>

    </div>
  )
}


export default About

