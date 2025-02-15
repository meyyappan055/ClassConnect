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
      <div className='font-inter font-semibold text-3xl text-center mt-20'>
        Why I Made ClassConnect?🧑‍💻
      </div>
      <div className='font-inter font-normal text-lg mt-10 ml-8 mr-8 md:ml-20 md:mr-20 leading-relaxed'>

        Back in my first year, my daily routine included a not-so-fun ritual: manually scheduling all my classes in Google Calendar📆.
        I’d flip between pages in academia or stare at a timetable image, then painstakingly add them to my calendar. Every. Single. Day.⌛

        <br /><br />

        It was boring, repetitive, and frustrating. I knew there had to be a smarter way.💡Around this time, I noticed my friends wishing for the same thing—a simpler, more efficient way to manage their schedules.  
        I even came across a public group 👥where someone explained how they relied on their calendar and needed a tool to simplify class scheduling.🛠️

        <br /><br />

        That’s when it clicked.⚡ If people, including me, needed this, why not create it? So I did. Welcome to ClassConnect. 🎉🚀

        <br /><br />

        Just download it, click on the file, and tap "Add All" - and boom! 💥  
              Your Weekly Timetable is ready 🎯📅 and your classes will instantly appear in your calendar.   
              It’s that easy!✅ 

      </div>

      <div className=''>
        <div className='font-inter font-semibold text-3xl text-center mt-20'>
          FAQs ❓💡
        </div>
          <div className='mx-10 md:mx-40 mt-10'>
          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>📅 How do I add it to my Calendar?</AccordionTrigger>
              <AccordionContent>
                Click on download file, open it, and tap "Add All" - done!  
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-2">
              <AccordionTrigger>💻 What platforms does ClassConnect support?</AccordionTrigger>
              <AccordionContent>
                Works with Google Calendar, Apple Calendar, Outlook, and more.  
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-3">
              <AccordionTrigger>🔒 Can I trust ClassConnect with my data?</AccordionTrigger>
              <AccordionContent>
                Yes! Your data is never stored—it's only used to fetch your timetable.  
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-4">
              <AccordionTrigger>📩 Need help?</AccordionTrigger>
              <AccordionContent>
                Reach out anytime!  
                <br />

                Email: meyyappan055@gmail.com  

                <br />
                WhatsApp: +91 8903042799  
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Accordion type="single" collapsible>
            <AccordionItem value="item-5">
              <AccordionTrigger>🏖️ Does it handle holidays?</AccordionTrigger>
              <AccordionContent>
                Yes! If your college updates Academia’s Calendar, ClassConnect will reflect it.  
              </AccordionContent>
            </AccordionItem>
          </Accordion>

        </div>
      </div>
    </div>
  )
}

export default About
