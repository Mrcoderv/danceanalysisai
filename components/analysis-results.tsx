"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Award } from "lucide-react"
import { getScoreColor, getScoreBadge } from "@/utils/score-utils" // Added imports for getScoreColor and getScoreBadge

interface AnalysisResultsProps {
  data: any
  danceStyle?: string // Added dance style prop
}

export function AnalysisResults({ data, danceStyle }: AnalysisResultsProps) {
  const getStyleSpecificAnalysis = () => {
    const baseResults = {
      overallScore: 85,
      rhythm: 78,
      coordination: 92,
      balance: 80,
      fluidity: 88,
      suggestions: [],
      strengths: [],
      improvements: ["Rhythm consistency", "Dynamic range", "Facial expression"],
    }

    switch (danceStyle) {
      case "bhajan-nepali":
        return {
          ...baseResults,
          overallScore: 88,
          rhythm: 85,
          coordination: 90,
          balance: 92,
          fluidity: 85,
          suggestions: [
            "Focus on spiritual expression through hand gestures",
            "Maintain devotional posture throughout the performance",
            "Synchronize movements with traditional rhythms",
          ],
          strengths: ["Excellent traditional hand positions", "Good spiritual expression", "Proper devotional stance"],
        }
      case "ballet":
        return {
          ...baseResults,
          suggestions: [
            "Work on maintaining turnout in fifth position",
            "Focus on port de bras fluidity",
            "Improve arabesque line",
          ],
          strengths: ["Beautiful arm positions", "Good posture and alignment", "Graceful transitions"],
        }
      default:
        return {
          ...baseResults,
          suggestions: [
            "Work on maintaining consistent rhythm in the middle section",
            "Great coordination between upper and lower body movements",
            "Consider adding more dynamic arm movements for visual impact",
          ],
          strengths: [
            "Excellent balance throughout the routine",
            "Smooth transitions between movements",
            "Good spatial awareness",
          ],
        }
    }
  }

  const analysisResults = getStyleSpecificAnalysis()

  return (
    <div className="space-y-6">
      {danceStyle && (
        <Card className="border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-900/20">
          <CardContent className="pt-6">
            <div className="text-center">
              <Badge variant="secondary" className="text-sm">
                Analyzing: {danceStyle.charAt(0).toUpperCase() + danceStyle.slice(1).replace("-", " ")} Style
              </Badge>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Overall Score */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5" />
            Overall Performance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center space-y-4">
            <div className={`text-4xl font-bold ${getScoreColor(analysisResults.overallScore)}`}>
              {analysisResults.overallScore}/100
            </div>
            <Badge {...getScoreBadge(analysisResults.overallScore)}>
              {getScoreBadge(analysisResults.overallScore).text}
            </Badge>
            <Progress value={analysisResults.overallScore} className="w-full" />
          </div>
        </CardContent>
      </Card>

      {/* ... existing code for other sections ... */}
    </div>
  )
}
