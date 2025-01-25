import React from 'react'
import { Button } from '../components/ui/button'
import { Link } from 'react-router-dom'
import { CircleChevronRight } from 'lucide-react';
import { CalendarCheck } from 'lucide-react';
import { CalendarSync } from 'lucide-react';
import { AlarmClockCheck } from 'lucide-react';
import Card from '@/components/Card'


const MainPage = () => {
  return (
    <section >
        <div className='mt-28 flex font-inter font-bold text-5xl justify-center items-center text-center'>
          Welcome to ClassConnect
        </div>

        <div className='mx-96 mt-6 flex font-inter font-semibold text-base justify-center items-center text-center text-gray-300'>
        Student life is busy—between lectures, assignments, and extracurriculars, managing your time can be tough. Class Connect makes scheduling effortless, keeping you on top of your classes.
        </div>

        <div className='flex justify-center mt-10 '>
          <Button variant="outline" className="font-semibold rounded-xl text-base p-5">
            <Link to="/login">Try it out</Link>
            <CircleChevronRight className="mr-1 h-5 w-5" />
          </Button>
        </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 sm:justify-items-center mt-24 px-4'>
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
          text = {"Your class schedule, available on all your devices through Google Calendar—anytime, anywhere."}
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