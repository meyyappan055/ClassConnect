import React from 'react'
import { Button } from '../components/ui/button'
import { Link } from 'react-router-dom'
import { CircleChevronRight } from 'lucide-react';
import { CalendarCheck } from 'lucide-react';
import { CalendarSync } from 'lucide-react';
import { AlarmClockCheck } from 'lucide-react';
import Card from '@/components/Card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"


const MainPage = () => {
  return (
    
  <section>
    
      <Dialog open={true}>
        <DialogContent className="max-w-md text-center">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold">BRB, Fixing Things! 🛠️ </DialogTitle>
          </DialogHeader>
          <p>Chill for a bit, I’ll have it back soon.</p>
          <Button variant="outline" className="mt-4" onClick={() => window.location.reload()}>
            Refresh Later
          </Button>
        </DialogContent>
      </Dialog>


        <div className='mt-28 flex font-inter font-bold text-3xl md:text-4-5xl justify-center items-center text-center'>
          Welcome to ClassConnect 📅
        </div>

        <div className='md:max-w-3xl px-10 mx-auto mt-6 flex font-inter font-semibold text-base justify-center items-center text-center text-gray-300'>
        Student life is busy—between lectures, assignments, and extracurriculars, managing your time can be tough. Class Connect makes scheduling effortless, keeping you on top of your classes.
        </div>

        <Link to="/login">
          <div className='flex justify-center mt-10 '>
            <Button variant="outline" className="font-semibold rounded-xl text-base p-5">
              Try it out
              <CircleChevronRight className="mr-1 h-5 w-5" />
            </Button>
          </div>
        </Link>
  
      <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 md:mx-8 mt-16 md:mt-24 px-4 overflow-hidden'>
        <div className=''>
          <Card 
          icon = {<CalendarCheck />}
          title = {"Effortless Scheduling"}
          text = {"Never juggle schedules again. Class times and dates at your fingertips."}
          />
        </div>


        <div className=''>
          <Card 
          icon = {<CalendarSync />}
          title = {"Stay Synchronized Across All Devices"}
          text = {"Your class schedule, available on all your devices through your Calendar—anytime, anywhere."}
          />
        </div>


        <div className=''>
          <Card 
          icon = {<AlarmClockCheck />}
          title = {"Timely Alerts, Every Time"}
          text = {"Get timely reminders for your upcoming classes and important events, so you're always prepared."}
          />
        </div>

        </div>

      </section>
  )
}

export default MainPage