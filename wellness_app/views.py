from django.shortcuts import render, redirect , get_object_or_404
from .models import UserHealthProfile, FitnessLog
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date , timedelta
from django.db.models import Avg, Sum
import json

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/dashboard/')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        msg = data.get('message', '').lower().strip()

        # ── GREETINGS ──────────────────────────────────────────
        if any(w in msg for w in ['hello', 'hlo', 'hi', 'hey', 'hii', 'hola', 'howdy', 'sup', 'what\'s up', 'wassup']):
            reply = "Hey! 👋 Welcome to Aromi AI! I'm your personal fitness & health assistant. You can ask me about workouts, diet plans, weight loss, muscle gain, injuries, sleep, mental health and more. What's on your mind today?"

        elif any(w in msg for w in ['hey bro', 'bro', 'buddy', 'mate', 'dude']):
            reply = "Hey bro! 💪 What's up? Ask me anything about fitness, diet, or health — I got you!"

        elif any(w in msg for w in ['good morning', 'morning']):
            reply = "Good morning! ☀️ Great time to start the day right. Have you had your water yet? Drink at least 500ml first thing in the morning — it kickstarts your metabolism!"

        elif any(w in msg for w in ['good night', 'night', 'goodnight']):
            reply = "Good night! 🌙 Remember — sleep is when your muscles actually grow and recover. Aim for 7–9 hours. No screens 30 mins before bed for better sleep quality!"

        elif any(w in msg for w in ['how are you', 'how r u', 'how are u', 'how do you do']):
            reply = "I'm doing great, thanks for asking! 😄 More importantly — how are YOU doing? Staying consistent with your workouts and diet? Let me know if you need any help!"

        elif any(w in msg for w in ['thank', 'thanks', 'thank you', 'thx', 'ty']):
            reply = "You're welcome! 🙌 Keep pushing, stay consistent and remember — every small step counts. Anything else I can help you with?"

        elif any(w in msg for w in ['bye', 'goodbye', 'see you', 'cya', 'later']):
            reply = "Goodbye! 💪 Stay consistent, eat clean, train hard. See you soon — Aromi AI is always here when you need it!"

        # ── WEIGHT LOSS ────────────────────────────────────────
        elif any(w in msg for w in ['lose weight', 'weight loss', 'fat loss', 'reduce weight', 'slim down', 'burn fat', 'how to lose', 'losing weight']):
            reply = ("🔥 Weight Loss Tips from Aromi AI:\n\n"
            "1. Create a calorie deficit of 300–500 kcal/day\n"
            "2. Eat high protein (1.6–2g per kg bodyweight)\n"
            "3. Do 3–4 days of strength training + 2 days cardio\n"
            "4. Drink 2.5–3L of water daily\n"
            "5. Sleep 7–9 hours — poor sleep increases hunger hormones\n"
            "6. Cut processed sugar, fried food, and liquid calories\n"
            "7. Eat more vegetables, lean protein, and whole grains\n\n"
            "💡 Tip: Don't crash diet! Sustainable weight loss is 0.5–1kg per week.")

        elif any(w in msg for w in ['belly fat', 'stomach fat', 'reduce belly', 'flat stomach', 'lose belly']):
            reply = ("🎯 How to Reduce Belly Fat:\n\n"
            "You cannot spot-reduce fat — but here's what works:\n"
            "1. Full body strength training 3–4x per week\n"
            "2. HIIT cardio 2x per week (20 mins is enough)\n"
            "3. Reduce refined carbs and sugar completely\n"
            "4. Manage stress — cortisol directly causes belly fat storage\n"
            "5. Sleep at least 7 hours — sleep deprivation increases belly fat\n"
            "6. Eat more fibre: oats, fruits, vegetables, legumes\n\n"
            "⚡ Core exercises like planks and crunches tone muscles but diet is 80% of the result!")

        # ── MUSCLE GAIN ────────────────────────────────────────
        elif any(w in msg for w in ['build muscle', 'gain muscle', 'muscle gain', 'bulk up', 'get big', 'get stronger', 'mass gain', 'bulking']):
            reply = ("💪 Muscle Building Guide:\n\n"
            "1. Eat in a calorie surplus (300–500 kcal above maintenance)\n"
            "2. Protein target: 1.8–2.2g per kg bodyweight daily\n"
            "3. Train each muscle group 2x per week\n"
            "4. Focus on progressive overload — increase weight/reps weekly\n"
            "5. Best muscle building foods: eggs, chicken, paneer, dal, milk, fish\n"
            "6. Sleep 8 hours — 80% of muscle growth happens during sleep\n"
            "7. Don't skip rest days — muscles grow during recovery, not training\n\n"
            "🏋️ Best exercises: Squats, Deadlifts, Bench Press, Pull-ups, Rows")

        elif any(w in msg for w in ['protein', 'protein intake', 'how much protein', 'protein diet', 'protein food']):
            reply = ("🥚 Protein Guide:\n\n"
            "Daily protein targets:\n"
            "• Weight loss: 1.6g per kg bodyweight\n"
            "• Muscle gain: 2–2.2g per kg bodyweight\n"
            "• General health: 1.2–1.4g per kg bodyweight\n\n"
            "Best protein sources:\n"
            "🥩 Chicken breast (31g per 100g)\n"
            "🥚 Eggs (6g per egg)\n"
            "🧀 Paneer (18g per 100g)\n"
            "🐟 Fish/Tuna (25g per 100g)\n"
            "🫘 Dal/Lentils (9g per 100g cooked)\n"
            "🥛 Greek Yoghurt (10g per 100g)\n"
            "🌱 Tofu (8g per 100g)\n\n"
            "💡 Spread protein across all meals for best absorption!")

        # ── DIET & NUTRITION ───────────────────────────────────
        elif any(w in msg for w in ['daily meal','diet plan', 'meal plan', 'what to eat', 'diet chart', 'food plan', 'eating plan']):
            reply = ("🥗 Sample Daily Diet Plan (Aromi AI):\n\n"
            "🌅 Breakfast (7–8 AM):\n"
            "   Oats + banana + 2 boiled eggs + black coffee\n\n"
            "🍎 Mid-Morning Snack (10:30 AM):\n"
            "   Fruits + handful of nuts or Greek yoghurt\n\n"
            "☀️ Lunch (1 PM):\n"
            "   2 rotis + dal/chicken + sabzi + salad + curd\n\n"
            "⚡ Pre-Workout Snack (4:30 PM):\n"
            "   Banana + peanut butter OR roasted chana\n\n"
            "🌙 Dinner (7:30–8 PM):\n"
            "   Grilled protein + vegetables + light roti/khichdi\n\n"
            "💧 Water: 2.5–3L throughout the day\n"
            "🚫 Avoid: Fried food, sugar, packaged snacks, cold drinks")

        elif any(w in msg for w in ['calorie', 'calories', 'how many calories', 'calorie intake', 'calorie deficit']):
            reply = ("🔥 Calorie Guide:\n\n"
            "Your daily calorie needs depend on your weight, height, age and activity level.\n\n"
            "General estimates:\n"
            "• Sedentary person: ~1800–2000 kcal/day\n"
            "• Moderately active: ~2200–2500 kcal/day\n"
            "• Very active/athlete: ~2800–3500 kcal/day\n\n"
            "For goals:\n"
            "🔻 Weight loss: eat 300–500 kcal BELOW your maintenance\n"
            "🔺 Muscle gain: eat 300–500 kcal ABOVE your maintenance\n"
            "➡️ Maintenance: eat at your exact calorie needs\n\n"
            "💡 Track your food using apps like MyFitnessPal for accuracy!")

        elif any(w in msg for w in ['vegetarian', 'vegan', 'plant based', 'no meat', 'vegetarian diet']):
            reply = ("🌱 Vegetarian Fitness Diet:\n\n"
            "Best vegetarian protein sources:\n"
            "• Paneer, tofu, tempeh\n"
            "• Dal, rajma, chana, moong\n"
            "• Eggs (if eggetarian)\n"
            "• Greek yoghurt, cottage cheese\n"
            "• Quinoa, soya chunks\n"
            "• Milk and whey protein\n\n"
            "Sample day:\n"
            "Breakfast: Moong dal chilla + curd\n"
            "Lunch: Rajma + brown rice + salad\n"
            "Dinner: Paneer bhurji + 2 rotis + sabzi\n\n"
            "💡 Combine different plant proteins in the same meal for complete amino acid profile!")

        elif any(w in msg for w in ['water', 'hydration', 'how much water', 'drink water']):
            reply = ("💧 Hydration Guide:\n\n"
            "Daily water target: 35ml × your bodyweight in kg\n"
            "Example: 70kg person → 2.45L per day\n\n"
            "When to drink:\n"
            "• 500ml warm water first thing in morning\n"
            "• 1 glass 30 mins before each meal\n"
            "• 500ml–1L during workout\n"
            "• Sip throughout the day, don't chug all at once\n\n"
            "Signs of dehydration:\n"
            "😴 Fatigue  🤕 Headache  😵 Dizziness  🟡 Dark urine\n\n"
            "💡 Add lemon or cucumber to water if plain water feels boring!")

        # ── WORKOUTS ───────────────────────────────────────────
        elif any(w in msg for w in ['workout', 'exercise', 'gym', 'training', 'workout plan', 'exercise plan', 'gym plan']):
            reply = ("🏋️ Weekly Workout Plan (Aromi AI):\n\n"
            "Monday: 💪 Chest & Triceps\n"
            "Tuesday: 🦵 Legs & Glutes\n"
            "Wednesday: 🧘 Active Rest (yoga/walk)\n"
            "Thursday: 🏋️ Back & Biceps\n"
            "Friday: 🫀 Cardio & Core\n"
            "Saturday: 🏃 Full Body or Sport\n"
            "Sunday: 😴 Complete Rest\n\n"
            "💡 Beginners: Start with 3 days/week full body\n"
            "💡 Intermediate: 4 day upper/lower split\n"
            "💡 Advanced: 5–6 day push/pull/legs\n\n"
            "Always warm up 5–10 mins before training!")

        elif any(w in msg for w in ['cardio', 'running', 'jogging', 'treadmill', 'cycling', 'swimming']):
            reply = ("🏃 Cardio Guide:\n\n"
            "Types of cardio:\n"
            "• LISS (Low Intensity): Walking, light cycling — 45–60 mins\n"
            "• HIIT (High Intensity): Sprints, burpees — 20–25 mins\n"
            "• Moderate: Jogging, swimming — 30–40 mins\n\n"
            "For weight loss: 3–4 cardio sessions per week\n"
            "For endurance: 4–5 sessions, gradually increase duration\n"
            "For heart health: 150 mins moderate cardio per week minimum\n\n"
            "💡 Do cardio AFTER weights, not before — you'll preserve more muscle!")

        elif any(w in msg for w in ['push up', 'pushup', 'pull up', 'pullup', 'squat', 'deadlift', 'plank', 'home workout', 'no gym']):
            reply = ("🏠 Home Workout — No Equipment Needed:\n\n"
            "Upper Body:\n"
            "• Push-ups: 4 × 15 (chest, shoulders, triceps)\n"
            "• Diamond Push-ups: 3 × 10 (triceps focus)\n"
            "• Pike Push-ups: 3 × 12 (shoulder focus)\n\n"
            "Lower Body:\n"
            "• Squats: 4 × 20\n"
            "• Lunges: 3 × 15 each leg\n"
            "• Glute Bridges: 4 × 20\n\n"
            "Core:\n"
            "• Plank: 3 × 60 seconds\n"
            "• Crunches: 3 × 20\n"
            "• Mountain Climbers: 3 × 30\n\n"
            "💡 Do this circuit 3x per week with 1 rest day between sessions!")

        # ── HEALTH ISSUES ──────────────────────────────────────
        elif any(w in msg for w in ['i have headache','headache', 'head pain', 'migraine', 'head ache']):
            reply = ("🤕 Headache Relief:\n\n"
            
            "• Low blood sugar\n"
            "• Too much screen time\n"
            "• Poor sleep\n"
            "• Overtraining\n\n"
            "Immediate relief:\n"
            "1. Drink 500ml water right now\n"
            "2. Eat a small snack if you haven't eaten\n"
            "3. Rest in a dark, quiet room\n"
            "4. Apply cold/warm compress on forehead\n"
            "5. Light neck stretching\n\n"
            "⚠️ If headache is severe or persists over 24 hours, please see a doctor!")

        elif any(w in msg for w in ['fever', 'temperature', 'high temperature', 'body heat']):
            reply = ("🌡️ Fever Management:\n\n"
            "Immediate steps:\n"
            "1. Rest completely — NO workout when you have fever\n"
            "2. Drink plenty of fluids (water, coconut water, ORS)\n"
            "3. Take paracetamol if temperature is above 38.5°C\n"
            "4. Apply cool wet cloth on forehead\n"
            "5. Wear light, breathable clothing\n\n"
            "Return to workout only after:\n"
            "• Fever is gone for at least 48 hours\n"
            "• You feel energetic and normal\n"
            "• Start back with 50% of your normal intensity\n\n"
            "⚠️ If fever exceeds 39.5°C or lasts more than 3 days — see a doctor immediately!")

        elif any(w in msg for w in ['tired', 'fatigue', 'exhausted', 'no energy', 'low energy', 'always tired', 'feeling weak', 'weakness']):
            reply = ("😴 Fighting Fatigue & Low Energy:\n\n"
            "Most common causes:\n"
            "• Poor sleep quality or less than 7 hours\n"
            "• Dehydration\n"
            "• Iron or Vitamin D deficiency\n"
            "• Overtraining without enough rest\n"
            "• Poor nutrition / skipping meals\n"
            "• High stress levels\n\n"
            "Energy boosters:\n"
            "1. Sleep 7–9 hours consistently\n"
            "2. Drink water first thing in morning\n"
            "3. Eat iron-rich foods: spinach, dates, red meat, beans\n"
            "4. Take Vitamin D supplement if deficient\n"
            "5. Take rest days seriously — overtraining causes fatigue\n"
            "6. Reduce caffeine after 2pm — it destroys sleep quality\n\n"
            "⚠️ If fatigue persists despite good sleep and diet, get a blood test done!")

        elif any(w in msg for w in ['pain', 'muscle pain', 'body pain', 'sore', 'soreness', 'doms', 'muscle soreness']):
            reply = ("💊 Muscle Pain & Soreness Relief:\n\n"
            "DOMS (Delayed Onset Muscle Soreness) is normal after workout!\n"
            "It peaks 24–72 hours after training and is a sign of muscle adaptation.\n\n"
            "Relief methods:\n"
            "1. Light walking or active recovery (don't stay still)\n"
            "2. Warm bath or heat therapy on sore muscles\n"
            "3. Foam rolling / massage — very effective\n"
            "4. Stay hydrated — 2.5L+ water daily\n"
            "5. Eat enough protein to aid muscle repair\n"
            "6. Light stretching — 10–15 mins\n\n"
            "⚠️ Difference between DOMS and injury:\n"
            "DOMS = dull ache in muscle, both sides, goes away in 3 days\n"
            "Injury = sharp/stabbing pain, one side, gets worse — see a doctor!")

        elif any(w in msg for w in ['back pain', 'lower back', 'back ache', 'spine']):
            reply = ("🦴 Back Pain Relief:\n\n"
            "Immediate steps:\n"
            "1. Rest — avoid heavy lifting for 48–72 hours\n"
            "2. Apply ice pack for first 24 hours (20 mins on, 20 off)\n"
            "3. Then switch to heat therapy\n"
            "4. Take anti-inflammatory if needed\n\n"
            "Exercises that help:\n"
            "• Cat-cow stretch\n"
            "• Child's pose\n"
            "• Knee-to-chest stretch\n"
            "• Dead bug exercise\n"
            "• Bird dog exercise\n\n"
            "Prevention:\n"
            "• Strengthen core — it protects your spine\n"
            "• Fix sitting posture (don't slouch)\n"
            "• Deadlift and squat with proper form\n\n"
            "⚠️ If pain shoots down your leg or is severe — see a doctor immediately!")

        elif any(w in msg for w in ['knee pain', 'knee', 'joint pain', 'joints']):
            reply = ("🦵 Knee Pain Guide:\n\n"
            "Common causes:\n"
            "• Bad squatting form (knees caving in)\n"
            "• Running on hard surfaces\n"
            "• Weak glutes and hip muscles\n"
            "• Overtraining / too much volume\n\n"
            "Immediate steps:\n"
            "1. RICE method: Rest, Ice, Compress, Elevate\n"
            "2. Avoid high impact exercises until pain subsides\n"
            "3. Switch to swimming or cycling temporarily\n\n"
            "Knee strengthening exercises:\n"
            "• Straight leg raises\n"
            "• Wall sits\n"
            "• Clamshells (for hip/glute strength)\n"
            "• Step-ups\n\n"
            "⚠️ Never train through sharp knee pain — you risk serious injury!")

        # ── SLEEP ──────────────────────────────────────────────
        elif any(w in msg for w in ['sleep', 'insomnia', 'cant sleep', 'not sleeping', 'sleep better', 'sleep problems']):
            reply = ("😴 Sleep Optimization Guide:\n\n"
            "Why sleep matters for fitness:\n"
            "• 80% of muscle growth happens during sleep\n"
            "• Poor sleep increases cortisol (fat storage hormone)\n"
            "• Sleep deprivation kills workout performance\n"
            "• Growth hormone is released during deep sleep\n\n"
            "Tips for better sleep:\n"
            "1. Sleep and wake at the same time every day\n"
            "2. No screens 1 hour before bed (blue light kills melatonin)\n"
            "3. Keep room cool and dark\n"
            "4. No caffeine after 2pm\n"
            "5. Magnesium supplement helps with deep sleep\n"
            "6. Light stretching or reading before bed\n"
            "7. Avoid heavy meals within 2 hours of sleep\n\n"
            "💡 Aim for 7–9 hours. Even 30 mins extra sleep improves performance!")

        # ── MENTAL HEALTH ──────────────────────────────────────
        elif any(w in msg for w in ['stress', 'anxiety', 'mental health', 'stressed', 'anxious', 'depression', 'sad', 'feeling low', 'not motivated', 'motivation']):
            reply = ("🧠 Mental Health & Fitness:\n\n"
            "Exercise is one of the most powerful antidepressants:\n"
            "• 20–30 mins of exercise releases endorphins naturally\n"
            "• Regular training reduces cortisol (stress hormone) by 40%\n"
            "• Yoga and meditation reduce anxiety significantly\n\n"
            "When motivation is low:\n"
            "1. Start with just 10 minutes — often you'll keep going\n"
            "2. Set tiny daily goals, not huge targets\n"
            "3. Find a workout buddy or community\n"
            "4. Track your progress — seeing improvement is motivating\n"
            "5. Listen to high-energy music during workout\n\n"
            "Daily habits for mental health:\n"
            "• 10 mins morning sunlight exposure\n"
            "• 5 mins of deep breathing/meditation\n"
            "• Limit social media to 30 mins/day\n"
            "• Journaling before sleep\n\n"
            "❤️ If you're feeling consistently low, please talk to someone you trust or a professional.")

        # ── SUPPLEMENTS ────────────────────────────────────────
        elif any(w in msg for w in ['supplement', 'whey', 'creatine', 'protein powder', 'pre workout', 'bcaa', 'vitamins']):
            reply = ("💊 Supplement Guide (Honest Advice):\n\n"
            "Worth it:\n"
            "✅ Whey Protein — convenient protein source, not magic\n"
            "✅ Creatine Monohydrate — proven for strength & muscle (5g/day)\n"
            "✅ Vitamin D3 — most Indians are deficient, important for everything\n"
            "✅ Omega-3 Fish Oil — reduces inflammation, great for joints\n"
            "✅ Magnesium — improves sleep quality and muscle recovery\n"
            "✅ Multivitamin — fills nutritional gaps in diet\n\n"
            "Not necessary:\n"
            "❌ Fat burners — mostly caffeine + marketing\n"
            "❌ Testosterone boosters — rarely work\n"
            "❌ Mass gainers — just expensive calories, eat real food instead\n\n"
            "💡 Food first, supplements second. No supplement replaces a good diet!")

        # ── BMI & WEIGHT ───────────────────────────────────────
        elif any(w in msg for w in ['bmi', 'body mass index', 'am i overweight', 'healthy weight', 'ideal weight']):
            reply = ("⚖️ BMI Guide:\n\n"
            "BMI Categories:\n"
            "• Below 18.5 → Underweight\n"
            "• 18.5 – 24.9 → Healthy Weight ✅\n"
            "• 25.0 – 29.9 → Overweight\n"
            "• 30.0 and above → Obese\n\n"
            "Calculate your BMI:\n"
            "BMI = Weight(kg) ÷ Height(m)²\n"
            "Example: 70kg ÷ (1.75 × 1.75) = 22.9 (Healthy!)\n\n"
            "⚠️ BMI has limitations:\n"
            "• Doesn't account for muscle mass\n"
            "• A muscular athlete may show 'overweight' BMI\n"
            "• Body fat % is a better measure than BMI alone\n\n"
            "💡 Your Aromi AI plan already calculated your BMI — check your plan page!")

        # ── DEFAULT ────────────────────────────────────────────
        else:
            reply = ("🤖 I'm not sure I understood that fully!\n\n"
            "Here's what I can help you with:\n"
            "💪 Workouts — gym plans, home workouts, cardio\n"
            "🥗 Diet — meal plans, calories, protein, nutrition\n"
            "⚖️ Weight — weight loss, muscle gain, BMI\n"
            "🏥 Health — headache, fever, pain, fatigue, sleep\n"
            "🧠 Mental health — stress, motivation, anxiety\n"
            "💊 Supplements — whey, creatine, vitamins\n\n"
            "Try asking something like:\n"
            "• 'How do I lose belly fat?'\n"
            "• 'What should I eat to build muscle?'\n"
            "• 'Give me a workout plan'\n"
            "• 'I have knee pain, what should I do?'")

        return JsonResponse({'response': reply})

@login_required
def dashboard(request):
    user = request.user
    profile, created = UserHealthProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Save name to User model
        full_name = request.POST.get('full_name', '')
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name  = parts[1] if len(parts) > 1 else ''
            user.save()

        # Save profile
        profile.age        = request.POST.get('age')
        profile.height     = float(request.POST.get('height', 0))
        profile.weight     = float(request.POST.get('weight', 0))
        profile.goal       = request.POST.get('goal')
        profile.gender     = request.POST.get('gender', '')
        profile.activity   = request.POST.get('activity_level', '')
        profile.diet       = request.POST.get('diet_preference', '')
        profile.conditions = request.POST.get('health_conditions', '')
        profile.save()

        return redirect('plan')

    # New user — no age yet
    if profile.age is None:
        return render(request, 'newuserdash.html')

    # Existing user
    return redirect('plan')

@login_required
def plan(request):
    user = request.user
    
    try:
        profile = UserHealthProfile.objects.get(user=user)
    except UserHealthProfile.DoesNotExist:
        return redirect('dashboard')

    # Guard — if profile incomplete, send back
    if not profile.age:
        return redirect('dashboard')
    

    # Calculate BMI
    bmi = None
    bmi_status = ''
    if profile.height and profile.weight:
        h = float(profile.height) / 100
        bmi = round(float(profile.weight) / (h * h), 1)
        if   bmi < 18.5: bmi_status = 'Underweight'
        elif bmi < 25:   bmi_status = 'Healthy'
        elif bmi < 30:   bmi_status = 'Overweight'
        else:            bmi_status = 'Obese'

    # Calculate calorie target (Mifflin-St Jeor formula)
    calorie_target = 2000  # default
    if profile.age and profile.weight and profile.height:
        age = int(profile.age)
        w   = float(profile.weight)
        h   = float(profile.height)
        # BMR base
        if profile.gender == 'female':
            bmr = 10 * w + 6.25 * h - 5 * age - 161
        else:
            bmr = 10 * w + 6.25 * h - 5 * age + 5

        # Activity multiplier
        multipliers = {
            'sedentary': 1.2,
            'light':     1.375,
            'moderate':  1.55,
            'active':    1.725,
            'athlete':   1.9,
        }
        multiplier = multipliers.get(profile.activity, 1.375)
        tdee = bmr * multiplier

        # Adjust for goal
        if   profile.goal == 'weight_loss':   calorie_target = int(tdee - 400)
        elif profile.goal == 'muscle_gain':   calorie_target = int(tdee + 300)
        else:                                 calorie_target = int(tdee)

    # Water target (35ml per kg bodyweight)
    water_target = round(float(profile.weight) * 0.035, 1) if profile.weight else 2.5

    # Protein target (~1.8g per kg for active goals)
    protein_target = int(float(profile.weight) * 1.8) if profile.weight else 120

    context = {
        'profile':        profile,
        'bmi':            bmi,
        'bmi_status':     bmi_status,
        'calorie_target': f"{calorie_target:,}",
        'water_target':   water_target,
        'protein_target': protein_target,
        'workout_days':   4,
        'goal':           profile.goal,
        'diet':           profile.diet,
        'age':            profile.age,
        'weight':         profile.weight,
        'height':         profile.height,
    }
    return render(request, 'plan.html', context)



@login_required
def log_activity(request):
    user = request.user
    profile = get_object_or_404(UserHealthProfile, user=user)
    today = date.today()
    existing = FitnessLog.objects.filter(user=user, date=today).first()

    if request.method == "POST":
        if existing:
            log = existing
        else:
            log = FitnessLog(user=user, date=today)

        log.weight    = request.POST.get('weight') or None
        log.calories  = request.POST.get('calories') or None
        log.steps     = request.POST.get('steps') or None
        log.water     = request.POST.get('water') or None
        log.workout   = request.POST.get('workout', '')
        log.duration  = request.POST.get('duration') or None
        log.intensity = request.POST.get('intensity', '')
        log.mood      = request.POST.get('mood') or None
        log.notes     = request.POST.get('notes', '')
        log.save()
        return redirect('progress')

    context = {
        'profile':         profile,
        'existing':        existing,
        'today':           today,
        'workout_choices': FitnessLog.WORKOUT_CHOICES,  # ← add this
    }
    return render(request, 'log.html', context)


@login_required
def progress(request):
    user = request.user
    profile = get_object_or_404(UserHealthProfile, user=user)

    # Last 30 days logs
    thirty_days_ago = date.today() - timedelta(days=29)
    logs = FitnessLog.objects.filter(
        user=user,
        date__gte=thirty_days_ago
    ).order_by('date')

    # ── Chart Data ──────────────────────────────────────
    dates      = [log.date.strftime('%d %b') for log in logs]
    weights    = [float(log.weight) if log.weight else None for log in logs]
    calories   = [log.calories if log.calories else 0 for log in logs]
    steps      = [log.steps if log.steps else 0 for log in logs]
    water      = [float(log.water) if log.water else 0 for log in logs]
    moods      = [log.mood if log.mood else 0 for log in logs]

    # ── Summary Stats ───────────────────────────────────
    total_logs      = FitnessLog.objects.filter(user=user).count()
    total_calories  = FitnessLog.objects.filter(user=user).aggregate(Sum('calories'))['calories__sum'] or 0
    avg_water       = FitnessLog.objects.filter(user=user).aggregate(Avg('water'))['water__avg'] or 0
    avg_steps       = FitnessLog.objects.filter(user=user).aggregate(Avg('steps'))['steps__avg'] or 0

    # ── Streak calculation ───────────────────────────────
    streak = 0
    check  = date.today()
    all_dates = set(
        FitnessLog.objects.filter(user=user)
        .values_list('date', flat=True)
    )
    while check in all_dates:
        streak += 1
        check -= timedelta(days=1)

    # ── Latest weight ────────────────────────────────────
    latest_log = FitnessLog.objects.filter(
        user=user, weight__isnull=False
    ).first()
    current_weight = latest_log.weight if latest_log else profile.weight

    # ── Weight change ────────────────────────────────────
    old_log = FitnessLog.objects.filter(
        user=user, weight__isnull=False
    ).order_by('date').first()
    weight_change = None
    if old_log and current_weight:
        diff = round(float(current_weight) - float(old_log.weight), 1)
        weight_change = f"+{diff}" if diff > 0 else str(diff)

    # ── Recent 7 logs for history table ─────────────────
    recent_logs = FitnessLog.objects.filter(user=user)[:7]

    # ── BMI ──────────────────────────────────────────────
    bmi = None
    if profile.height and current_weight:
        h = float(profile.height) / 100
        bmi = round(float(current_weight) / (h * h), 1)

    context = {
        'profile':        profile,
        'logs':           logs,
        'recent_logs':    recent_logs,
        'total_logs':     total_logs,
        'total_calories': f"{int(total_calories):,}",
        'avg_water':      round(avg_water, 1),
        'avg_steps':      f"{int(avg_steps):,}",
        'streak':         streak,
        'current_weight': current_weight,
        'weight_change':  weight_change,
        'bmi':            bmi,
        # JSON for charts
        'chart_dates':    json.dumps(dates),
        'chart_weights':  json.dumps(weights),
        'chart_calories': json.dumps(calories),
        'chart_steps':    json.dumps(steps),
        'chart_water':    json.dumps(water),
        'chart_moods':    json.dumps(moods),
    }
   
    return render(request, 'progress.html', context)


@login_required
def history(request):
    user = request.user
    logs = FitnessLog.objects.filter(user=user)
    return render(request, 'history.html', {'logs': logs})

@login_required
def profile(request):
    return redirect('plan')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
