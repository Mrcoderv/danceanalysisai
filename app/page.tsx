"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, Camera, Music, Play, Square, Volume2 } from "lucide-react"
import { PoseDetector } from "@/components/pose-detector"
import { StickFigureCanvas } from "@/components/stick-figure-canvas"
import { AnalysisResults } from "@/components/analysis-results"

export default function DanceAnalysisPage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisProgress, setAnalysisProgress] = useState(0)
  const [currentPoses, setCurrentPoses] = useState<any[]>([])
  const [analysisData, setAnalysisData] = useState<any>(null)
  const [activeTab, setActiveTab] = useState("upload")

  const [musicFile, setMusicFile] = useState<File | null>(null)
  const [isMusicPlaying, setIsMusicPlaying] = useState(false)
  const [danceStyle, setDanceStyle] = useState<string>("")
  const [dancePercentage, setDancePercentage] = useState<number | null>(null)
  const [sessionStartTime, setSessionStartTime] = useState<number | null>(null)
  const [totalDanceTime, setTotalDanceTime] = useState(0)
  const [activeDanceTime, setActiveDanceTime] = useState(0)

  const audioRef = useRef<HTMLAudioElement>(null)
  const musicInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const danceStyles = [
    { value: "hip-hop", label: "🎤 Hip Hop", description: "Urban street dance with strong beats" },
    { value: "ballet", label: "🩰 Ballet", description: "Classical dance with graceful movements" },
    { value: "contemporary", label: "💃 Contemporary", description: "Modern expressive dance" },
    { value: "latin", label: "🌶️ Latin", description: "Passionate Latin American dances" },
    { value: "bhajan-nepali", label: "🙏 Bhajan Nepali", description: "Traditional Nepali devotional dance" },
  ]

  const handlePoseDetection = (poses: any[]) => {
    setCurrentPoses(poses)

    if (poses.length > 0 && isMusicPlaying) {
      const currentTime = Date.now()
      if (sessionStartTime) {
        const isActivelyDancing = poses.some((pose) => pose.keypoints.some((kp: any) => kp.confidence > 0.7))

        if (isActivelyDancing) {
          setActiveDanceTime((prev) => prev + 100) // Add 100ms of active dance time
        }
        setTotalDanceTime(currentTime - sessionStartTime)
      }
    }
  }

  const handleAnalysisComplete = (data: any) => {
    setAnalysisData(data)
    setIsAnalyzing(false)
    setAnalysisProgress(100)
  }

  const handleMusicUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && audioRef.current) {
      setMusicFile(file)
      const url = URL.createObjectURL(file)
      audioRef.current.src = url
      audioRef.current.load()
    }
  }

  const toggleMusic = () => {
    if (!audioRef.current || !musicFile) return

    if (isMusicPlaying) {
      // Stop music and calculate percentage
      audioRef.current.pause()
      setIsMusicPlaying(false)

      if (totalDanceTime > 0) {
        const percentage = Math.round((activeDanceTime / totalDanceTime) * 100)
        setDancePercentage(Math.min(percentage, 100))
      }

      setSessionStartTime(null)
    } else {
      // Start music and reset tracking
      audioRef.current.play()
      setIsMusicPlaying(true)
      setSessionStartTime(Date.now())
      setTotalDanceTime(0)
      setActiveDanceTime(0)
      setDancePercentage(null)
      startAnalysis()
    }
  }

  const startAnalysis = () => {
    setIsAnalyzing(true)
    setAnalysisProgress(0)

    const interval = setInterval(() => {
      setAnalysisProgress((prev) => {
        if (prev >= 90) {
          clearInterval(interval)
          return 90
        }
        return prev + 10
      })
    }, 500)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Dance Analysis AI</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Upload your music and dance video or use live camera to get real-time pose analysis, movement scoring, and
            improvement suggestions powered by AI.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Music className="w-5 h-5" />
                Music Upload
              </CardTitle>
              <CardDescription>Upload your favorite music to dance to</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <input ref={musicInputRef} type="file" accept="audio/*" onChange={handleMusicUpload} className="hidden" />
              <Button onClick={() => musicInputRef.current?.click()} className="w-full" variant="outline">
                <Upload className="w-4 h-4 mr-2" />
                Choose Music File
              </Button>

              {musicFile && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Selected: {musicFile.name}</p>
                  <div className="flex gap-2">
                    <Button onClick={toggleMusic} className="flex-1">
                      {isMusicPlaying ? (
                        <>
                          <Square className="w-4 h-4 mr-2" />
                          Stop Music
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4 mr-2" />
                          Play Music
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              )}

              <audio ref={audioRef} loop />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Dance Style</CardTitle>
              <CardDescription>Select your dance style for better analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={danceStyle} onValueChange={setDanceStyle}>
                <SelectTrigger>
                  <SelectValue placeholder="Choose dance style" />
                </SelectTrigger>
                <SelectContent>
                  {danceStyles.map((style) => (
                    <SelectItem key={style.value} value={style.value}>
                      <div>
                        <div className="font-medium">{style.label}</div>
                        <div className="text-xs text-gray-500">{style.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>
        </div>

        {dancePercentage !== null && (
          <Card className="mb-8 border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-900/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-700 dark:text-green-300">
                <Volume2 className="w-5 h-5" />
                Dance Performance Result
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center space-y-4">
                <div className="text-6xl font-bold text-green-600 dark:text-green-400">{dancePercentage}%</div>
                <p className="text-lg text-green-700 dark:text-green-300">
                  You were actively dancing for {dancePercentage}% of the music duration!
                </p>
                <Progress value={dancePercentage} className="w-full" />
              </div>
            </CardContent>
          </Card>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <Upload className="w-4 h-4" />
              Upload Video
            </TabsTrigger>
            <TabsTrigger value="live" className="flex items-center gap-2">
              <Camera className="w-4 h-4" />
              Live Camera
            </TabsTrigger>
          </TabsList>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Video/Camera Input Section */}
            <div className="space-y-6">
              <TabsContent value="upload" className="mt-0">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Upload className="w-5 h-5" />
                      Video Upload
                    </CardTitle>
                    <CardDescription>Upload a dance video for analysis (MP4, MOV, AVI supported)</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <PoseDetector
                      mode="upload"
                      onPoseDetection={handlePoseDetection}
                      onAnalysisComplete={handleAnalysisComplete}
                      danceStyle={danceStyle}
                    />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="live" className="mt-0">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Camera className="w-5 h-5" />
                      Live Camera
                    </CardTitle>
                    <CardDescription>Use your camera for real-time dance analysis</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <PoseDetector
                      mode="camera"
                      onPoseDetection={handlePoseDetection}
                      onAnalysisComplete={handleAnalysisComplete}
                      danceStyle={danceStyle}
                    />
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Analysis Progress */}
              {isAnalyzing && (
                <Card>
                  <CardHeader>
                    <CardTitle>Analyzing Movement...</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Progress value={analysisProgress} className="mb-2" />
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Processing pose data and generating insights...
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Stick Figure Animation & Analysis */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Stick Figure Animation</CardTitle>
                  <CardDescription>Real-time visualization of detected poses</CardDescription>
                </CardHeader>
                <CardContent>
                  <StickFigureCanvas poses={currentPoses} width={400} height={300} />
                </CardContent>
              </Card>

              {analysisData && <AnalysisResults data={analysisData} danceStyle={danceStyle} />}
            </div>
          </div>
        </Tabs>
      </div>
    </div>
  )
}
