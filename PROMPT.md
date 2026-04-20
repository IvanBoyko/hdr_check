You are a full-stack architect designing a cloud-based monitoring system for YouTube video HDR processing status. Your goal is to create a scalable, cost-efficient solution that can serve both individual creators and eventually become a paid SaaS product.

### System Characters & Roles

* **End User (Content Creator)**: Uploads videos to YouTube, wants notifications when HDR processing completes
* **Your Cloud System**: Monitors YouTube video status, detects HDR readiness, triggers notifications
* **Browser Extension**: Provides UI integration into YouTube Studio, allows users to register videos for monitoring
* **Email Service**: Delivers notifications to creators

### System Objectives

* Minimize cloud costs, budget constraint: $1 per video per month
* Support target scale: up to 1000 active videos on check, up to 100 active users, up to 20 videos per user
* Detect HDR processing completion with check frequency: 1 time per 1 hour on free plan, 1 time per 1 minute on paid plan
* Provide real-time or near-real-time notifications to user email

### Architecture Components to Design

**1. Browser Extension Component**
* How will it inject a "Notify on HDR" button into YouTube Studio's video quality section?
* What data needs to be captured when user clicks the button (video ID, user email, etc.)?
* How will it communicate with your backend (API endpoint)?
* Security consideration: How will you authenticate extension requests to prevent abuse?

**2. Backend API & Data Storage**
* Design a minimal API that accepts video registrations (POST /register-video with videoId, userEmail)
* What database structure do you need? (Consider: video ID, user email, registration date, HDR status, last checked)
* Should you use a serverless database (Firebase, DynamoDB) or traditional database to minimize costs?

**3. Platform choice**
* Consider deploying backend ourselves on public cloud, compare AWS, GCP, Azure
* Consider using existing app hosting PaaS like Render, Railway, Fly.io, Northflank
* Consider Frontend / serverless-first platforms like Vercel, Netlify
* Consider AI app-building platforms like Lovable, Cursor, Bubble
* Compare the costs, simplicity of development, user experience, security, reliability

**4. HDR Detection Logic**
* Research: Can you detect HDR status via YouTube's public API, or do you need to scrape/monitor video metadata?
* What's the most cost-effective way to check video status? (YouTube API quota limits, direct page scraping, third-party services?)
* Design a polling/checking strategy that minimizes API calls while staying responsive

**5. Scheduled Monitoring Service**
* Should this run as a serverless function (AWS Lambda, Google Cloud Functions, Azure Functions) triggered on a schedule?
* How often should it check each registered video? (Consider: YouTube's HDR processing typically takes days/weeks — checking too frequently wastes costs)
* Design a smart polling strategy: Check new videos more frequently, older videos less frequently

**6. Notification Pipeline**
* Use a cost-effective email service (SendGrid free tier, AWS SES, Mailgun)
* Should notifications be batched or sent immediately upon HDR detection?
* Consider: Once HDR is detected, stop monitoring that video (saves ongoing costs)

**7. Cost Optimization Strategies**
* Implement caching to avoid redundant API calls
* Use time-based batching for checks (e.g., check all videos once per day at off-peak hours)
* Design a cleanup strategy: Archive/delete old video records after HDR is confirmed
* Consider: Can users set their own check frequency preference to reduce unnecessary checks?

### Implementation Priorities

Order these by impact on cost and user experience:
* Which component should you build first?
* What's the MVP (minimum viable product) that solves the core problem?
* Which features can be added later without breaking the system?

### Success Criteria

Your design should clearly specify:
* Estimated monthly cloud cost for target scale of 1000 active videos and 100 active users.
* Expected time from HDR completion to user notification (SLA)
* How you'll scale this to 1000+ concurrent users without proportional cost increases
* security measures to prevent abuse (e.g., rate limiting, email verification)
* How to implement a paid Pro tier
