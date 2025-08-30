"use client"

import type React from "react"

import { useRef, useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Upload, Play, Pause, RotateCcw } from "lucide-react"

interface PoseDetectorProps {
  mode: "upload" | "camera"
  onPoseDetection: (poses: any[]) => void
  onAnalysisComplete: (data: any) => void
  danceStyle?: string // Added dance style prop
}

export function PoseDetector({ mode, onPoseDetection, onAnalysisComplete, danceStyle }: PoseDetectorProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const videoUrl = URL.createObjectURL(file)
      videoRef.current!.src = videoUrl
      videoRef.current!.load()
    }
  }

  const togglePlayback = () => {
    if (videoRef.current) {
      if (videoRef.current.paused || videoRef.current.ended) {
        videoRef.current.play()
        setIsPlaying(true)
      } else {
        videoRef.current.pause()
        setIsPlaying(false)
      }
    }
  }

  const resetVideo = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0
    }
  }

  const startPoseDetection = () => {
    const detectPoses = () => {
      if (!isPlaying || !videoRef.current) return

      // Mock pose data with style-specific variations
      const getStyleSpecificPoses = () => {
        const basePose = {
          keypoints: [
            { x: 320, y: 100, confidence: 0.9, name: "nose" },
            { x: 300, y: 150, confidence: 0.8, name: "left_shoulder" },
            { x: 340, y: 150, confidence: 0.8, name: "right_shoulder" },
            { x: 280, y: 200, confidence: 0.7, name: "left_elbow" },
            { x: 360, y: 200, confidence: 0.7, name: "right_elbow" },
            { x: 260, y: 250, confidence: 0.6, name: "left_wrist" },
            { x: 380, y: 250, confidence: 0.6, name: "right_wrist" },
            { x: 310, y: 280, confidence: 0.8, name: "left_hip" },
            { x: 330, y: 280, confidence: 0.8, name: "right_hip" },
            { x: 300, y: 350, confidence: 0.7, name: "left_knee" },
            { x: 340, y: 350, confidence: 0.7, name: "right_knee" },
            { x: 290, y: 420, confidence: 0.6, name: "left_ankle" },
            { x: 350, y: 420, confidence: 0.6, name: "right_ankle" },
          ],
        }

        // Modify poses based on dance style
        if (danceStyle === "bhajan-nepali") {
          // Traditional hand positions for devotional dance
          basePose.keypoints[5].y = 180 // left_wrist higher
          basePose.keypoints[6].y = 180 // right_wrist higher
          basePose.keypoints[5].confidence = 0.9
          basePose.keypoints[6].confidence = 0.9
        } else if (danceStyle === "ballet") {
          // Graceful arm positions
          basePose.keypoints[5].y = 200
          basePose.keypoints[6].y = 200
        }

        return [basePose]
      }

      const mockPoses = getStyleSpecificPoses()
      onPoseDetection(mockPoses)

      // Continue detection
      if (isPlaying) {
        requestAnimationFrame(detectPoses)
      }
    }

    detectPoses()
  }

  useEffect(() => {
    if (mode === "camera") {
      setIsLoading(true)
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          setStream(stream)
          videoRef.current!.srcObject = stream
          videoRef.current!.play()
          setIsPlaying(true)
          setIsLoading(false)
        })
        .catch((error) => {
          console.error("Error accessing camera:", error)
          setIsLoading(false)
        })
    }
  }, [mode])

  return (
    <div className="space-y-4">
      {mode === "upload" && (
        <div className="space-y-4">
          <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileUpload} className="hidden" />
          <Button onClick={() => fileInputRef.current?.click()} className="w-full" variant="outline">
            <Upload className="w-4 h-4 mr-2" />
            Choose Video File
          </Button>
        </div>
      )}

      <div className="relative bg-black rounded-lg overflow-hidden">
        <video ref={videoRef} className="w-full h-64 object-cover" muted playsInline />
        <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full pointer-events-none" />
      </div>

      <div className="flex gap-2 justify-center">
        <Button onClick={togglePlayback} size="sm">
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </Button>
        <Button onClick={resetVideo} size="sm" variant="outline">
          <RotateCcw className="w-4 h-4" />
        </Button>
      </div>

      {isLoading && <p className="text-center text-sm text-gray-600 dark:text-gray-400">Loading camera...</p>}
    </div>
  )
}
