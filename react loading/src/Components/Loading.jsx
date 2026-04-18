import {useEffect, useState} from "react";
export default function Loading ({complating, setComplating}) {
    const [count, setCount] = useState(0);
            useEffect(() => {
                if (complating) {
                    const interval = setInterval(() => {
                        setCount(prev => {
                            if (prev >= 100) {
                                clearInterval(interval);
                                setComplating(true);
                                return 100;
                            }
                            return prev + 1
                        }); 
                    }, 25);
                    return () => clearInterval(interval)
                }
            },  [complating]);
    return (
        <div className="modal_2">
            <div className="PreLoader">
                <div className="text">
                    <div>{count === 100 ? "Yakunlandi." : (
                        <div>Sayt yuklanmoqda<span className="dot dot1">.</span><span className="dot dot2">.</span><span className="dot dot3">.</span></div>)}
                    </div>
                    <p>{count}%</p>
                </div>
                <div className="bar">
                    <div className="bar_in" style={{width: `${count}%`}}></div>
                </div>
            </div>
        </div>
    )
}