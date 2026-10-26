import Navbar from './components/Navbar'
import Hero from './components/Hero'
import CourseCatalog from './components/CourseCatalog'
import LearningPath from './components/LearningPath'
import Stories from './components/Stories'
import DemoBooking from './components/DemoBooking'
import Faq from './components/Faq'
import Footer from './components/Footer'

export default function App() {
  return (
    <>
      <a href="#courses" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-lg focus:bg-white focus:px-4 focus:py-2">
        Skip to courses
      </a>
      <Navbar />
      <main>
        <Hero />
        <CourseCatalog />
        <LearningPath />
        <Stories />
        <Faq />
        <DemoBooking />
      </main>
      <Footer />
    </>
  )
}
