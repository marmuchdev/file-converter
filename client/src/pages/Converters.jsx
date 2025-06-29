import { Link } from 'react-router-dom'

     function Converters() {
       return (
         <div className="text-center">
           <h1 className="text-3xl font-bold mb-6">Available Converters</h1>
           <ul className="space-y-4">
             <li>
               <Link
                 to="/converters/json-to-pdf"
                 className="text-blue-600 hover:text-blue-800 text-lg"
               >
                 JSON to PDF
               </Link>
             </li>
           </ul>
         </div>
       )
     }

     export default Converters