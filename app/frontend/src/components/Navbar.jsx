import React from 'react'
import { LogIn } from 'lucide-react';
import { House } from 'lucide-react';
import { Info } from 'lucide-react';
import { CalendarClock } from 'lucide-react';
import { Github } from 'lucide-react';
import {Link} from 'react-router-dom';


const Navbar = () => {
  return (
    <nav className='flex justify-between'>
        <div className='mt-3 ml-3 flex flex-row'>
            <div><CalendarClock className="h-6 w-6 mt-1 mr-2" /></div>
            <h2 className='text-2xl font-inter font-bold text-white'>ClassConnect</h2>    
        </div>   

        <div className='mt-5 mr-1 '>
            <Link to="https://github.com/meyyappan055/ClassConnect">
                <button>
                    {<Github className="mr-4 h-5 w-5 hover:bg-white/10" />}
                </button>
            </Link>

            <Link to="/">
                <button>
                    {<House className="mr-4 h-5 w-5 hover:bg-white/10" />}
                </button>
            </Link>

            <Link to="/login">
                <button>
                    {<LogIn className="mr-4 h-5 w-5 hover:bg-white/10 " />}
                </button>
            </Link>

            <Link to="/about">
                <button>
                    {<Info className="mr-4 h-5 w-5 hover:bg-white/10" />}
                </button>
            </Link>
        </div>
    </nav>
  )
}

export default Navbar