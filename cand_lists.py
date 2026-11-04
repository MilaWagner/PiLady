P='coverr-'
B=[
 # b0 intro: thinking
 "contemplative-woman-with-windswept-hair thinking-on-a-mountain-top-152 contemplative-woman-in-the-park contemplative-young-woman-in-park businesswoman-contemplating-in-city-park contemplative-woman-at-seashore contemplative-woman-by-the-roadside contemplative-woman-in-city".split(),
 # b1 books / origin
 "cozy-outdoor-reading-time tranquil-outdoor-reading-session serene-reading-time-by-the-seashore solitude-by-the-sea-reading-time relaxing-beachside-reading-session man-reading-a-book-in-his-jungle-home-849 girl-writing-in-a-notebook-2268 teenager-writing-in-a-notebook-1062 writing-poetry-7787 creative-writing-session-outdoors focused-writing-session-outdoors inspiring-outdoor-journaling-session old-man-drawing-in-a-notebook-7324 ancient-roman-general-in-deep-thought".split(),
 # b2 hypotheses / study
 "focused-student-studying-outdoors focused-outdoor-study-session girl-studying-in-a-cafe-6193 student-working-at-her-home-office-8091 student-sitting-at-her-desk-in-her-home-office-3995 artist-sketching-seaside-scenery old-man-drawing-in-his-notebook-3712 examining-plants-4318 girl-drawing-in-a-notebook-7110 student-typing-on-her-laptop-8175".split(),
 # b3 survey / film
 "walking-through-a-crowd-7633 crowded-park-in-paris-5830 timelapse-of-a-crowded-crosswalk-1120 friends-talking-at-a-restaurant-8705 popcorn-flying-from-a-box-with-a-red-background-9217 a-striped-colored-black-box-slowly-falls-and-popcorn-falls-out-3024 old-man-watching-tv-on-the-couch-9269 families-at-the-park-4617 people-say-hi-on-a-video-call-3316 coworkers-talk-on-a-video-conference-9226 an-old-man-sitting-on-the-couch-watching-television-358 crowded-bridge-8424".split(),
 # b4 body functions
 "girl-practicing-open-air-yoga-4945 a-man-stretches-his-shoulders-6042 girl-stretching-during-yoga-practice-2017 casual-chat-by-the-van surfers-chatting-by-the-ocean woman-chatting-by-her-car-trunk taking-vitamins-230 outdoor-morning-crunch-workout twilight-stretching-routine active-lifestyle-outdoor-exercise".split(),
 # b5 energy
 "urban-wellness-city-jogging urban-running-in-the-evening seaside-morning-run woman-running-down-a-road-8310 woman-eating-healthy-food-8374 eating-avocado-and-egg-on-toast-5170 woman-shopping-for-fresh-produce healthy-snack-time-outdoors hands-picking-up-olives-4485 urban-runner-catching-her-breath evening-runner-catching-her-breath woman-running-outdoors-3013".split(),
 # b6 scanning / always active
 "the-city-at-night-2412 houston-texas-at-night-4130 evening-city-landscape-4349 night-city-from-a-moving-car-6550 cars-in-the-city-at-night-5837 gloomy-city-at-night-6099 high-voltage-power-line-tower-against-blue-sky lighting-up-a-sparkler-6510 women-waving-sparklers-around-5334 girl-lying-on-a-hammock-6062 woman-lying-in-a-hammock-7731 woman-relaxing-on-her-bed-5442 driving-past-a-building-at-night-9184 twilight-city-call".split(),
 # b7 potential: practice
 "skateboarder-practicing-on-a-mini-ramp-7525 skater-practicing-9077 outdoor-fitness-session-with-dumbbells outdoor-dumbbell-workout-session girl-takes-a-selfie-whilst-studying-5971 man-using-his-laptop-outdoors-9659 using-laptop-on-the-street-4292 ready-for-fitness-outdoors".split(),
 # b8 summary: sunrise sunset
 "woman-watching-the-sunset-5104 woman-enjoying-the-sunshine-2892 ai-generated-sunset-rays-above-the-clouds sunset-over-the-atlantic-ocean-1409 seaside-serenity-woman-relaxing-on-beach walking-to-the-mountain-top-8360 hiking-through-the-mountains-1755 peaceful-break-in-the-woods tranquil-forest-break-with-hiker".split(),
 # b9 outro
 "the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore-3079 woman-spinning-around-6948 taking-a-selfie-in-the-sunlight-3787 couple-watching-the-sunset-together-4048 road-in-the-mountains-7132".split(),
]
CANDS=[[P+s for s in b] for b in B]
